# Clear Browser Storage

## To Clear the Dark Theme Cache

Since we reverted the theme changes, you need to clear your browser's localStorage to remove any cached theme settings.

### Quick Fix - Run in Browser Console

1. Open Browser DevTools (F12 or Cmd+Option+I on Mac)
2. Go to **Console** tab
3. Copy and paste this command:

```javascript
localStorage.clear();
document.documentElement.classList.remove('dark');
document.documentElement.className = '';
location.reload();
```

4. Press Enter
5. Page will reload with proper light theme

## Alternative Method

1. Open Browser DevTools (F12)
2. Go to **Application** tab (Chrome) or **Storage** tab (Firefox)
3. Find **Local Storage** → `http://localhost:3000`
4. Right-click and select **Clear**
5. Reload the page

## What This Does

- Removes the cached 'dark' theme value
- Removes the 'dark' class from HTML element
- Clears any other localStorage data
- Reloads the page fresh

After this, the application will work normally with the standard light theme (no dark mode).

## Verification

After clearing, you should see:
- White backgrounds
- Dark text
- Blue sidebar
- Normal light theme throughout

The Settings page will show "Dark (Soon)" and "Auto (Soon)" as disabled placeholders again.

