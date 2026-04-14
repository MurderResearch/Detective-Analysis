'use strict';

function ts() {
  return new Date().toISOString();
}

function fmt(level, args) {
  const parts = args.map((a) =>
    typeof a === 'string' ? a : JSON.stringify(a, null, 2)
  );
  return `[${ts()}] [${level}] ${parts.join(' ')}`;
}

const logger = {
  info: (...args) => console.log(fmt('INFO', args)),
  warn: (...args) => console.warn(fmt('WARN', args)),
  error: (...args) => console.error(fmt('ERROR', args)),
  debug: (...args) => {
    if (process.env.NODE_ENV !== 'production') {
      console.log(fmt('DEBUG', args));
    }
  },
};

module.exports = logger;
