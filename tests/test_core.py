"""Network-free tests for the core, plugin generator and extensions."""
import json
from pathlib import Path

import pytest
from rich.console import Console

from labsecurity_core.console import LabsecurityConsole
from labsecurity_core.executor import Executor
from labsecurity_core.generator import create_plugin, import_script, install_plugin
from labsecurity_core.models import Option, PluginError
from labsecurity_core.registry import Registry
from labsecurity_core.ui import Output

ROOT = Path(__file__).resolve().parents[1]


def app_for(root: Path) -> tuple[LabsecurityConsole, object]:
    from io import StringIO
    stream = StringIO()
    out = Output(Console(file=stream, force_terminal=False, highlight=False, width=145))
    return LabsecurityConsole(root, out), stream


def test_original_scripts_migrated_as_plugins():
    registry = Registry(ROOT / 'plugins')
    assert not registry.errors
    assert len(registry.modules) == 9
    assert registry.modules['auxiliary/dns/infodns'].options['DOMAIN'].required
    assert 'doctor' in registry.commands


def test_empty_core_has_no_plugins(tmp_path):
    app, stream = app_for(tmp_path)
    app.execute_line('search')
    assert not app.registry.modules
    app.execute_line('help')
    assert 'Core commands' in stream.getvalue()


def test_set_unset_required_validation():
    app, stream = app_for(ROOT)
    app.execute_line('use auxiliary/scanner/scanport')
    app.execute_line('run')
    assert 'Required options missing: RHOSTS, RPORT' in stream.getvalue()
    app.execute_line('set RPORT 99999')
    assert 'must be between' in stream.getvalue()
    app.execute_line('set RHOSTS 127.0.0.1')
    app.execute_line('set RPORT 80')
    assert app.settings['auxiliary/scanner/scanport']['RPORT'] == 80
    app.execute_line('unset RPORT')
    assert app.settings['auxiliary/scanner/scanport']['RPORT'] is None


def test_search_index_and_extension_command():
    app, stream = app_for(ROOT)
    app.execute_line('search dns')
    assert app.last_search
    app.execute_line('use 0')
    assert app.selected is not None
    app.execute_line('back')
    app.execute_line('doctor')
    assert 'Python runtime:' in stream.getvalue()


def test_plugin_generation_and_execution(tmp_path):
    path = create_plugin(tmp_path / 'plugins', 'hello')
    assert path.exists()
    app, stream = app_for(tmp_path)
    app.execute_line('use auxiliary/custom/hello')
    app.execute_line('set TARGET "Hello, world"')
    app.execute_line('run')
    assert 'Plugin executed.' in stream.getvalue()
    assert app.selected.id == 'auxiliary/custom/hello'


def test_legacy_import_static_copy_and_execution(tmp_path):
    legacy = tmp_path / 'some_script.py'
    legacy.write_text('def run(target):\n    print("IMPORTED", target)\n', encoding='utf-8')
    folder = import_script(tmp_path / 'plugins', legacy)
    assert (folder / 'legacy_script.py').read_text(encoding='utf-8') == legacy.read_text(encoding='utf-8')
    app, _ = app_for(tmp_path)
    app.execute_line('use auxiliary/legacy/some_script')
    app.execute_line('set TARGET example.org')
    # Running prints from legacy code; no external side effects in our fixture.
    app.execute_line('run')
    assert app.selected.id == 'auxiliary/legacy/some_script'


def test_legacy_import_not_run_during_generation(tmp_path):
    marker = tmp_path / 'owned.txt'
    source = tmp_path / 'unsafe.py'
    source.write_text(f'from pathlib import Path\nPath({str(marker)!r}).write_text("bad")\ndef run(): pass\n')
    import_script(tmp_path / 'plugins', source)
    assert not marker.exists()


def test_command_conflict_is_rejected(tmp_path):
    folder = create_plugin(tmp_path / 'plugins', 'tool')
    manifest = folder / 'manifest.json'
    raw = json.loads(manifest.read_text())
    raw['commands'] = [{'name': 'run', 'description': 'overrides core', 'entrypoint': 'plugin.py:run'}]
    manifest.write_text(json.dumps(raw))
    registry = Registry(tmp_path / 'plugins')
    assert 'run' not in registry.commands
    assert any('reserved' in item for item in registry.errors)


def test_untrusted_paths_rejected(tmp_path):
    with pytest.raises(PluginError):
        create_plugin(tmp_path / 'plugins', '../escape')
    with pytest.raises(PluginError):
        create_plugin(tmp_path / 'plugins', 'my-plugin')
    folder = create_plugin(tmp_path / 'plugins', 'normal')
    raw = json.loads((folder / 'manifest.json').read_text())
    raw['entrypoint'] = '../outside.py:run'
    (folder / 'manifest.json').write_text(json.dumps(raw))
    registry = Registry(tmp_path / 'plugins')
    assert not registry.modules
    assert registry.errors


def test_option_conversion():
    assert Option.from_dict({'name':'ENABLED','type':'boolean','default':False}).convert('yes') is True
    with pytest.raises(PluginError):
        Option.from_dict({'name':'PAGE','type':'url'}).convert('file:///etc/passwd')
    assert Option.from_dict({'name':'WHAT','type':'choice','choices':['a','b']}).convert('a') == 'a'


def test_reload_reads_updated_plugin_source(tmp_path):
    folder = create_plugin(tmp_path / 'plugins', 'reloaded')
    app, stream = app_for(tmp_path)
    app.execute_line('use auxiliary/custom/reloaded')
    app.execute_line('set TARGET example.org')
    app.execute_line('run')
    assert 'Plugin executed.' in stream.getvalue()
    (folder / 'plugin.py').write_text('def run(ctx):\n    ctx.success("NEW IMPLEMENTATION")\n')
    app.execute_line('reload')
    app.execute_line('run')
    assert 'NEW IMPLEMENTATION' in stream.getvalue()


def test_port_parser_limits_are_strict():
    import importlib.util
    script = ROOT / 'plugins/auxiliary/scanner/scanports/plugin.py'
    spec = importlib.util.spec_from_file_location('tests_ports', script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module._ports('22,80,443-445') == [22, 80, 443, 444, 445]
    with pytest.raises(ValueError):
        module._ports('1-100000000')


def test_install_complete_plugin_folder(tmp_path):
    source = create_plugin(tmp_path / 'foreign_plugins', 'imported')
    destination = install_plugin(tmp_path / 'current' / 'plugins', source)
    assert (destination / 'manifest.json').exists()
    app, output = app_for(tmp_path / 'current')
    app.execute_line('use auxiliary/custom/imported')
    assert app.selected.id == 'auxiliary/custom/imported'
    with pytest.raises(PluginError):
        install_plugin(tmp_path / 'current' / 'plugins', source)
