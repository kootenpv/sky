<h1> sky </h1>

The following should be done:

```python
pip install -r requirements.txt
```

Make sky available globally by adding:

```python
export PYTHONPATH=$PYTHONPATH:/path/to/this/clone/sky
```

to your `.bashrc`

or instead on a "per session basis" use:

```python
import sys
sys.path.append('/path/to/this/clone/sky')
```

to be able to `import sky`.