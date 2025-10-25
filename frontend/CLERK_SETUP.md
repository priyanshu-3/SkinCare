# Clerk Authentication Setup Guide

This guide will walk you through setting up Clerk authentication for the Skin Cancer Detection React frontend.

## Prerequisites

- Node.js 18+ installed
- A Clerk account (free tier available)

## Step 1: Create a Clerk Application

1. Go to [https://dashboard.clerk.com](https://dashboard.clerk.com)
2. Sign up or log in
3. Click "Create Application"
4. Choose your authentication methods (recommended: Email, Google)
5. Name your application (e.g., "Skin Cancer Detection")

## Step 2: Get Your Publishable Key

1. In your Clerk Dashboard, go to **API Keys** page
2. Select **React** from the framework dropdown
3. Copy your **Publishable Key** (starts with `pk_test_` or `pk_live_`)

## Step 3: Configure Environment Variables

1. Open the file `frontend/.env.local`
2. Replace `YOUR_PUBLISHABLE_KEY` with your actual Clerk Publishable Key:

```bash
VITE_CLERK_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

3. Save the file

## Step 4: Install Dependencies & Run

```bash
cd frontend
npm install
npm run dev
```

The app should now be running at `http://localhost:5173`

## Step 5: Test Authentication

1. Open your browser to `http://localhost:5173`
2. Click "Get Started" or "Sign In"
3. Complete the sign-up process
4. You should see the `UserButton` in the header after signing in

## Features Included

### Authentication Components
- ✅ `<SignInButton>` - Opens sign-in modal
- ✅ `<SignUpButton>` - Opens sign-up modal
- ✅ `<UserButton>` - User profile dropdown
- ✅ `<SignedIn>` - Shows content only when signed in
- ✅ `<SignedOut>` - Shows content only when signed out

### Protected Routes
- `/` - Public home page
- `/analysis` - Protected (requires sign-in)
- `/results` - Protected (requires sign-in)

## Customization

### Change Sign-Out Redirect

In `src/main.jsx`, modify the `afterSignOutUrl` prop:

```jsx
<ClerkProvider publishableKey={PUBLISHABLE_KEY} afterSignOutUrl="/custom-url">
```

### Add More Auth Options

In Clerk Dashboard → User & Authentication → Email, Phone, Username:
- Enable/disable authentication methods
- Configure OAuth providers (Google, GitHub, etc.)
- Customize sign-up fields

### Customize Appearance

```jsx
<ClerkProvider
  publishableKey={PUBLISHABLE_KEY}
  appearance={{
    baseTheme: dark, // or light
    variables: { colorPrimary: '#3b82f6' }
  }}
>
```

## Troubleshooting

### Error: "Missing Clerk Publishable Key"
- Ensure `.env.local` exists in the `frontend/` directory
- Verify the key starts with `VITE_CLERK_PUBLISHABLE_KEY=`
- Restart the dev server after changing environment variables

### Sign-in modal doesn't open
- Check browser console for errors
- Ensure `@clerk/clerk-react` is installed
- Clear browser cache and reload

### Authentication state not persisting
- Check if cookies are enabled in your browser
- Verify you're using the same domain/port
- Check Clerk Dashboard → Sessions settings

## Security Notes

1. **Never commit `.env.local`** - It's already in `.gitignore`
2. **Use `pk_test_` keys for development only**
3. **Use `pk_live_` keys for production**
4. The `VITE_` prefix exposes the key to client-side code (this is safe for Clerk's publishable keys)

## Production Deployment

1. Add `VITE_CLERK_PUBLISHABLE_KEY` to your deployment platform's environment variables
2. Use your production Clerk key (starts with `pk_live_`)
3. Configure allowed domains in Clerk Dashboard → Settings → Domains

## Resources

- [Clerk React Quickstart](https://clerk.com/docs/quickstarts/react)
- [Clerk React SDK Reference](https://clerk.com/docs/references/react/overview)
- [Clerk Dashboard](https://dashboard.clerk.com)

## Support

If you encounter issues:
1. Check the [Clerk documentation](https://clerk.com/docs)
2. Visit [Clerk's Discord community](https://clerk.com/discord)
3. Review the [Clerk React examples](https://github.com/clerk/clerk-react-examples)

