/**
 * TypeScript Analyzer Fixtures
 *
 * These files serve as regression anchors for the TypeScript compiler and ESLint.
 * Any change that causes these fixtures to fail type-checking or linting indicates
 * an analyzer regression.
 *
 * Purpose:
 * - Catch breaking changes in tsconfig.json compiler options
 * - Detect ESLint rule regressions
 * - Verify path alias resolution (@/...)
 * - Ensure Jest global types remain available
 */

// --- Fixture 1: Path Alias Resolution ---
// This import MUST resolve without errors. If it fails, the @/ path alias is broken.
import { env } from '@/env'
import { getCurrentUser } from '@/lib/fanvue'

// --- Fixture 2: Type Inference ---
// Verify that TypeScript correctly infers types from complex expressions
const inferredNumber: number = 42
const inferredString: string = 'sky-os-framework'
const inferredBoolean: boolean = true
const inferredArray: string[] = ['alpha', 'beta', 'gamma']
const inferredObject: { name: string; version: number } = { name: 'SkyOS', version: 4 }

// --- Fixture 3: Optional Chaining & Nullish Coalescing ---
const maybeNull: string | null = null
const maybeUndefined: number | undefined = undefined

const safeAccess = (maybeNull as string | null)?.length
const fallbackValue = maybeUndefined ?? 0

// --- Fixture 4: Async/Await Patterns ---
async function asyncFixture(): Promise<string> {
  return 'fixture-result'
}

// --- Fixture 5: Generic Types ---
type Result<T> = {
  data: T
  error: string | null
  timestamp: number
}

const stringResult: Result<string> = {
  data: 'test',
  error: null,
  timestamp: Date.now(),
}

const numberResult: Result<number> = {
  data: 42,
  error: null,
  timestamp: Date.now(),
}

// --- Fixture 6: Union & Intersection Types ---
type Status = 'idle' | 'loading' | 'success' | 'error'

interface BaseConfig {
  id: string
}

interface ExtendedConfig extends BaseConfig {
  timeout: number
  retries: number
}

const config: ExtendedConfig = {
  id: 'test-config',
  timeout: 5000,
  retries: 3,
}

// --- Fixture 7: Discriminated Unions ---
type Action =
  | { type: 'ADD'; payload: number }
  | { type: 'REMOVE'; payload: number }
  | { type: 'RESET' }

function handleAction(action: Action): void {
  switch (action.type) {
    case 'ADD':
      console.log(action.payload)
      break
    case 'REMOVE':
      console.log(action.payload)
      break
    case 'RESET':
      console.log('reset')
      break
  }
}

// --- Fixture 8: Environment Variable Types ---
// Verify that @t3-oss/env-nextjs types are correctly resolved
const oauthClientId: string = env.OAUTH_CLIENT_ID
const apiBaseUrlStr: string = env.API_BASE_URL.toString()

// --- Fixture 9: Function Overloads ---
function parse(input: string): number
function parse(input: number): number
function parse(input: string | number): number {
  return typeof input === 'string' ? parseInt(input, 10) : input
}

// --- Fixture 10: Readonly & Const Assertions ---
const readonlyArray: readonly string[] = ['immutable', 'array'] as const
const readonlyObj: Readonly<{ key: string }> = { key: 'value' }

// Exports for import testing
export {
  inferredNumber,
  inferredString,
  inferredBoolean,
  inferredArray,
  inferredObject,
  safeAccess,
  fallbackValue,
  asyncFixture,
  stringResult,
  numberResult,
  config,
  handleAction,
  oauthClientId,
  apiBaseUrlStr,
  parse,
  readonlyArray,
  readonlyObj,
}

export type {
  Result,
  Status,
  BaseConfig,
  ExtendedConfig,
  Action,
}
