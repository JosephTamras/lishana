import { test, expect } from '@playwright/test';

test.describe('Search Functionality', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display search box on page load', async ({ page }) => {
    const searchInput = page.locator('input[placeholder*="Search"]');
    await expect(searchInput).toBeVisible();
  });

  test('should search and display results', async ({ page }) => {
    const searchInput = page.locator('input[placeholder*="Search"]');
    
    // Type in search box
    await searchInput.fill('dog');
    
    // Wait for results
    await page.waitForLoadState('networkidle');
    
    // Check if results are displayed
    const results = page.locator('a[href*="/word/"]');
    await expect(results.first()).toBeVisible();
  });

  test('should clear search and show empty state', async ({ page }) => {
    const searchInput = page.locator('input[placeholder*="Search"]');
    
    // Search for something
    await searchInput.fill('test');
    await page.waitForLoadState('networkidle');
    
    // Clear search
    await searchInput.clear();
    
    // Verify empty state message
    const emptyMessage = page.locator('text=Start typing to search');
    await expect(emptyMessage).toBeVisible();
  });

  test('should navigate to word detail when clicked', async ({ page }) => {
    const searchInput = page.locator('input[placeholder*="Search"]');
    
    // Search for a word
    await searchInput.fill('word');
    await page.waitForLoadState('networkidle');
    
    // Click first result
    const firstResult = page.locator('a[href*="/word/"]').first();
    await firstResult.click();
    
    // Verify navigation to word page
    await expect(page).toHaveURL(/\/word\/\d+/);
  });
});
