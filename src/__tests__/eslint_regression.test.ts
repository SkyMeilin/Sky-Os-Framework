/**
 * ESLint Regression Test
 *
 * This test verifies that the ESLint golden file passes without any warnings
 * or errors. It catches regressions in ESLint configuration.
 */

import { execSync } from 'child_process'
import { existsSync } from 'fs'
import { join } from 'path'

describe('ESLint Analyzer Regression', () => {
  const goldenFilePath = join(__dirname, 'fixtures', 'eslint_golden.ts')

  it('golden file exists', () => {
    expect(existsSync(goldenFilePath)).toBe(true)
  })

  it('golden file passes ESLint without warnings', () => {
    // This test runs ESLint on the golden file and expects 0 warnings/errors
    try {
      const result = execSync(
        `npx eslint "${goldenFilePath}" --format json`,
        { encoding: 'utf-8', stdio: 'pipe' }
      )

      const reports = JSON.parse(result) as Array<{ messages?: Array<{ ruleId: string }> }>
      const messages = reports.flatMap((r: { messages?: Array<{ ruleId: string }> }) => r.messages || [])

      expect(messages).toHaveLength(0)
    } catch (error) {
      // ESLint exits with code 1 on warnings/errors
      // We want to fail the test if this happens
      throw error
    }
  })
})
