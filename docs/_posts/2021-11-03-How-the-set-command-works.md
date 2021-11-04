---
layout: post
description: The set command is a command that allows us to select something specific, but we must think that set means to select in order to have an idea of how that command would work.
---

The ```set``` command is a command that allows us to select something specific, but we must think that ```set``` means to select in order to have an idea of how that command would work.

For example, if we want to select a target we would have to use the ```set``` command and then place ```target```:

```shell
set target 127.0.0.1
```

In this way we will have selected the objective. The ip that has been selected is after the ```target```, when we use ```target``` in ```set``` we are indicating that what is going to be selected is a target such as an ip or a host.

And in the end the ip will have been stored in the ```target``` variable and we can check that by executing the same command since we will get a message and that indicates that the target was stored in the variable.

If we wanted to select a port we would have to use the command ```set``` and then ```port``` since we specify that we are going to select a port by putting ```set port``` and an example would be ```set port 80``` where we would be selecting port 80.

# Summary

<h2 id="how-the-set-command-works">How the set command works</h2>

<p>The <code class="language-plaintext highlighter-rouge">set</code> command allows you to select something, for example with <code class="language-plaintext highlighter-rouge">set target</code>, we select a target, but the complete command would be <code class="language-plaintext highlighter-rouge">set target 192.168.1.1</code>, with that we would be selecting the target’s ip.</p>

<p>But to select a port, <code class="language-plaintext highlighter-rouge">set port</code> is used, and an example would be <code class="language-plaintext highlighter-rouge">set port 80</code>, with which we would be selecting port 80.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>
set =&gt; select something for example a target
target or port =&gt; indicates the type of selection, if it is a target or a port, an example would be that the target is the ip.
example.com =&gt; here we would replace example.com with the target's ip or port

</code></pre></div></div>
