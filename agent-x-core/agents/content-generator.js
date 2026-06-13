/**
 * Agent: Content Generator
 * Responsibility: Produce deliverables for publishing: copy, posts, emails.
 * Revenue use: outreach, SEO drafts, affiliate-ready summaries.
 */

function respond(envelope) {
  const out = JSON.stringify(envelope);
  process.stdout.write(out + '\n');
}

function drafts({ topic, audience, tone = 'professional', variant = 'short' }) {
  const title = topic + ': ' + audience + ' briefing';
  const shortCopy = [
    'Quick take for ' + audience + ': ' + topic + ' matters now.',
    'Actionable angle: validate demand first, then ship.'
  ].join('\n\n');

  const longCopy = [
    'Context\n ' + topic + ' is relevant in today’s market.',
    'Evidence\n Demand signals support higher engagement.',
    'Implication\n ' + audience + ' can position faster with a derivative offer.',
    'Action\n Test one asset (post/email/list) before scaling.'
  ].join('\n\n');

  const body = variant === 'short' ? shortCopy : longCopy;
  const draft = { title, body, outline: ['Context', 'Evidence', 'Action'], tags: [topic, audience] };
  return draft;
}

function run(action, payload) {
  payload = payload || {};
  if (action === 'draft') {
    return { ok: true, result: drafts(payload) };
  }
  return { ok: false, error: 'Unknown action: ' + action };
}

process.stdin.setEncoding('utf8');
let buffer = '';
process.stdin.on('data', function(chunk) {
  buffer += chunk;
  while (buffer.indexOf('\n') !== -1) {
    const line = buffer.slice(0, buffer.indexOf('\n'));
    buffer = buffer.slice(buffer.indexOf('\n') + 1);
    if (!line.trim()) continue;
    let envelope;
    try {
      envelope = JSON.parse(line);
    } catch (e) {
      respond({ ok: false, error: 'Invalid JSON input' });
      continue;
    }
    const action = envelope.action;
    const payload = envelope.payload || {};
    const result = run(action, payload);
    respond({ ok: true, requestId: envelope.requestId || null, ...result });
  }
});
