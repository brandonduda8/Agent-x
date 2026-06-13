import subprocess
import sys
import json


def run_agent_once(agent_path, envelope):
    cmd = [sys.executable, agent_path] if str(agent_path).endswith('.py') else ['node', agent_path]
    child = subprocess.run(
        cmd,
        input=json.dumps(envelope) + '\n',
        capture_output=True,
        text=True,
        check=False,
    )
    raw = (child.stdout or '').strip()
    if not raw:
        return {'ok': False, 'error': 'empty-stdout', 'stderr': child.stderr.strip()}
    try:
        return json.loads(raw.splitlines()[-1])
    except Exception as e:
        return {'ok': False, 'error': f'bad-json:{e}', 'raw': raw}


if __name__ == '__main__':
    import os
    base = os.path.expanduser('~/agent-x/agent-x-core/agents')
    sample = {
        'action': 'draft',
        'requestId': 'cli-demo',
        'payload': {'topic': 'automation', 'audience': 'founders', 'variant': 'short'},
    }
    path = os.path.join(base, 'content-generator.js')
    print(json.dumps({'agent': path, 'result': run_agent_once(path, sample)}, indent=2))
