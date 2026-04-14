'use strict';

const config = require('./config');
const logger = require('./utils/logger');
const { runOnce } = require('./poller');

/**
 * CLI 進入點。
 *   node src/index.js            # 跑一次 poll 後結束（給 cron / launchd）
 *   node src/index.js --watch    # 常駐，每 INTERVAL_MINUTES 分鐘跑一次
 *   node src/index.js --dry-run  # 只會抓資料和印 log，不呼叫 FB 回覆
 */

const args = process.argv.slice(2);
const WATCH = args.includes('--watch');
const DRY = args.includes('--dry-run');
if (DRY) process.env.DRY_RUN = 'true';

async function main() {
  logger.info('fb-reply-bot start', {
    mode: WATCH ? 'watch' : 'one-shot',
    dryRun: !!process.env.DRY_RUN,
    provider: config.llm.provider,
    intervalMinutes: config.poller.intervalMinutes,
  });

  if (!WATCH) {
    try {
      await runOnce();
      process.exit(0);
    } catch (err) {
      logger.error('runOnce fatal', err.stack || err.message);
      process.exit(1);
    }
  }

  // watch mode：立即跑一次，之後用 setInterval 排下一次
  const loop = async () => {
    try {
      await runOnce();
    } catch (err) {
      logger.error('runOnce error', err.stack || err.message);
    }
  };
  await loop();
  const ms = config.poller.intervalMinutes * 60 * 1000;
  setInterval(loop, ms);
  logger.info(`watch mode: next poll in ${config.poller.intervalMinutes} min`);
}

process.on('SIGINT', () => {
  logger.info('SIGINT, bye');
  process.exit(0);
});

main();
