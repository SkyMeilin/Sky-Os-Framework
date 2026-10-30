/**
 * Analyzer Benchmark Reference Set
 *
 * This file defines the baseline performance expectations for all analyzers
 * in the CI pipeline. These values serve as the reference for detecting
 * performance regressions.
 *
 * Last updated: 2026-10-30
 * Environment: GitHub Actions ubuntu-latest runner
 */

const BENCHMARK_REFS = {
  // TypeScript compiler (tsc --noEmit)
  typescript: {
    // Maximum allowed compilation time for the entire src/ directory (seconds)
    maxCompilationTime: 30,
    // Expected: 0 errors
    expectedErrors: 0,
    // Expected: 0 type errors
    expectedTypeErrors: 0,
  },

  // ESLint
  eslint: {
    // Maximum allowed lint time for the entire src/ directory (seconds)
    maxLintTime: 15,
    // Expected: 0 warnings on golden files
    expectedGoldenWarnings: 0,
    // Expected: 0 errors
    expectedErrors: 0,
  },

  // Jest tests
  jest: {
    // Maximum allowed test execution time (seconds)
    maxTestTime: 60,
    // Expected: 0 failed tests
    expectedFailures: 0,
  },

  // Python flake8
  flake8: {
    // Maximum allowed lint time for all Python files (seconds)
    maxLintTime: 10,
    // Expected: 0 errors on fixture files
    expectedFixtureErrors: 0,
  },

  // Python black
  black: {
    // Maximum allowed format check time (seconds)
    maxFormatTime: 10,
    // Expected: 0 formatting differences on fixtures
    expectedFormattingDiffs: 0,
  },

  // Python bandit (security scan)
  bandit: {
    // Maximum allowed scan time (seconds)
    maxScanTime: 15,
    // Expected: 0 high severity issues on fixtures
    expectedHighSeverity: 0,
  },
}

// Export for use in CI scripts and test validation
export default BENCHMARK_REFS
