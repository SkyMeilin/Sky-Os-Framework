/**
 * TypeScript Type Regression Test
 *
 * This test verifies that core TypeScript types remain stable and correctly inferred.
 * It catches regressions where type changes break existing code patterns.
 */

import {
  inferredNumber,
  inferredString,
  inferredBoolean,
  inferredArray,
  inferredObject,
  asyncFixture,
  stringResult,
  numberResult,
  config,
  handleAction,
  parse,
  readonlyArray,
  readonlyObj,
  Result,
  Action,
} from './fixtures/analyzer_types'

describe('TypeScript Analyzer Regression', () => {
  describe('Type Inference', () => {
    it('infers number type correctly', () => {
      expect(typeof inferredNumber).toBe('number')
      expect(inferredNumber).toBe(42)
    })

    it('infers string type correctly', () => {
      expect(typeof inferredString).toBe('string')
      expect(inferredString).toBe('sky-os-framework')
    })

    it('infers boolean type correctly', () => {
      expect(typeof inferredBoolean).toBe('boolean')
      expect(inferredBoolean).toBe(true)
    })

    it('infers array type correctly', () => {
      expect(Array.isArray(inferredArray)).toBe(true)
      expect(inferredArray).toHaveLength(3)
      expect(inferredArray).toEqual(['alpha', 'beta', 'gamma'])
    })

    it('infers object type correctly', () => {
      expect(typeof inferredObject).toBe('object')
      expect(inferredObject).toEqual({ name: 'SkyOS', version: 4 })
    })
  })

  describe('Generic Types', () => {
    it('creates Result<string> correctly', () => {
      expect(stringResult.data).toBe('test')
      expect(stringResult.error).toBeNull()
      expect(typeof stringResult.timestamp).toBe('number')
    })

    it('creates Result<number> correctly', () => {
      expect(numberResult.data).toBe(42)
      expect(numberResult.error).toBeNull()
      expect(typeof numberResult.timestamp).toBe('number')
    })
  })

  describe('Extended Types', () => {
    it('extends BaseConfig correctly', () => {
      expect(config.id).toBe('test-config')
      expect(config.timeout).toBe(5000)
      expect(config.retries).toBe(3)
    })
  })

  describe('Discriminated Unions', () => {
    it('handles ADD action', () => {
      const action: Action = { type: 'ADD', payload: 10 }
      handleAction(action)
      expect(action.type).toBe('ADD')
    })

    it('handles REMOVE action', () => {
      const action: Action = { type: 'REMOVE', payload: 5 }
      handleAction(action)
      expect(action.type).toBe('REMOVE')
    })

    it('handles RESET action', () => {
      const action: Action = { type: 'RESET' }
      handleAction(action)
      expect(action.type).toBe('RESET')
    })
  })

  describe('Function Overloads', () => {
    it('parses string to number', () => {
      expect(parse('42')).toBe(42)
    })

    it('passes through number', () => {
      expect(parse(42)).toBe(42)
    })
  })

  describe('Readonly Types', () => {
    it('creates readonly array', () => {
      expect(readonlyArray).toEqual(['immutable', 'array'])
      expect(readonlyArray.length).toBe(2)
    })

    it('creates readonly object', () => {
      expect(readonlyObj.key).toBe('value')
    })
  })

  describe('Async Functions', () => {
    it('returns Promise<string>', async () => {
      const result = await asyncFixture()
      expect(result).toBe('fixture-result')
    })
  })
})
