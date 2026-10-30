/**
 * ESLint Golden File
 *
 * This file contains code patterns that MUST pass ESLint without any warnings or errors.
 * It serves as a golden reference for the ESLint configuration.
 *
 * If any line in this file triggers an ESLint warning, it indicates a regression
 * in the ESLint rules or configuration.
 *
 * Run: npx eslint src/__tests__/fixtures/eslint_golden.ts
 * Expected: 0 warnings, 0 errors
 */

// --- Golden 1: Proper variable naming (camelCase) ---
const maxValue = 100
const userName = 'SkyMeilin'
const isConnected = true

// --- Golden 2: No unused variables ---
function calculateSum(a: number, b: number): number {
  const result = a + b
  return result
}

// --- Golden 3: No console.log in production code (exempted for fixtures) ---
// eslint-disable-next-line no-console
console.log('Golden fixture loaded')

// --- Golden 4: Proper async/await usage ---
async function fetchData(url: string): Promise<string> {
  const response = await fetch(url)
  const data = await response.text()
  return data
}

// --- Golden 5: No unreachable code ---
function checkValue(value: number): string {
  if (value > 0) {
    return 'positive'
  }
  return 'non-positive'
}

// --- Golden 6: Proper equality checks (=== not ==) ---
function isEqual(a: unknown, b: unknown): boolean {
  return a === b
}

// --- Golden 7: No duplicate imports ---
import { env } from '@/env'
import { getCurrentUser } from '@/lib/fanvue'

// --- Golden 8: Proper return type annotation ---
function greet(name: string): string {
  return `Hello, ${name}`
}

// --- Golden 9: No empty blocks ---
function processItems(items: string[]): string[] {
  const processed: string[] = []
  for (const item of items) {
    if (item.length > 0) {
      processed.push(item.toUpperCase())
    }
  }
  return processed
}

// --- Golden 10: Proper switch statement with default ---
function getStatusColor(status: 'idle' | 'loading' | 'success' | 'error'): string {
  switch (status) {
    case 'idle':
      return 'gray'
    case 'loading':
      return 'blue'
    case 'success':
      return 'green'
    case 'error':
      return 'red'
    default:
      return 'white'
  }
}

// --- Golden 11: No self assignment ---
function updateValue(obj: { x: number }): void {
  obj.x = obj.x + 1
}

// --- Golden 12: Proper array methods ---
const numbers = [1, 2, 3, 4, 5]
const doubled = numbers.map((n) => n * 2)
const evens = numbers.filter((n) => n % 2 === 0)

// --- Golden 13: No sparse arrays ---
const denseArray = [1, 2, 3]

// --- Golden 14: Proper object literal syntax ---
const config = {
  host: 'localhost',
  port: 8080,
  enabled: true,
}

// --- Golden 15: No with statements ---
function safeAccess(obj: Record<string, unknown>, key: string): unknown {
  return obj[key]
}

// Exports to prevent "unused import" warnings
export {
  maxValue,
  userName,
  isConnected,
  calculateSum,
  fetchData,
  checkValue,
  isEqual,
  greet,
  processItems,
  getStatusColor,
  updateValue,
  doubled,
  evens,
  denseArray,
  config,
  safeAccess,
}
