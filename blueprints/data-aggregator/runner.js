#!/usr/bin/env node
/**
 * Blueprint: data aggregation microservice
 * - fetches source URLs
 * - collapses into summary artifacts
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');

async function runAggregation({ sourceUrls = [], timeWindow = '24h', metric = 'enriched' }) {
  const out = {
    sourceCount: sourceUrls.length,
    metric,
    timeWindow,
    sampled: await fetchSources(sourceUrls),
    generatedAt: new Date().toISOString()
  };

  const artifactDir = path.join(__dirname, '../../digital-twin/artifacts');
  fs.mkdirSync(artifactDir, { recursive: true });
  const file = path.join(artifactDir, 'latest-data-aggregate.json');
  fs.writeFileSync(file, JSON.stringify(out, null, 2), 'utf8');

  return out;
}

async function fetchSources(urls, limit = 10) {
  const results = [];
  for (const url of urls.slice(0, limit)) {
    try {
      const resp = await axios.get(url, { timeout: 10_000 });
      results.push({ url, ok: true, status: resp.status });
    } catch (e) {
      results.push({ url, ok: false, error: e.message });
    }
  }
  return results;
}

module.exports = { runAggregation };
