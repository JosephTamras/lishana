# Typesense InstantSearch Setup Guide

## Installation Complete ✅

Your Next.js app now has InstantSearch.js with the Typesense adapter configured for querying your local Typesense server.

## Packages Installed

- `instantsearch.js` - Core search UI library
- `react-instantsearch` - React components for InstantSearch
- `react-instantsearch-nextjs` - Next.js integration
- `typesense-instantsearch-adapter` - Typesense adapter for InstantSearch

## Configuration

### 1. Set up environment variables

Copy the example file and update with your Typesense server details:

```bash
cp .env.local.example .env.local
```

Then edit `.env.local`:

```env
# Typesense Configuration
NEXT_PUBLIC_TYPESENSE_HOST=localhost
NEXT_PUBLIC_TYPESENSE_PORT=8108
NEXT_PUBLIC_TYPESENSE_PROTOCOL=http
NEXT_PUBLIC_TYPESENSE_API_KEY=your-api-key
NEXT_PUBLIC_TYPESENSE_COLLECTION_NAME=your-collection-name
```

### 2. File Structure

- `app/components/SearchBox.tsx` - Main search component using react-instantsearch
- `app/page.tsx` - Updated home page with the SearchBox component

## Using the Search Component

The SearchBox component is already integrated into your homepage. It includes:

- **Search Input** - Type to search your Typesense collection
- **Hit Results** - Displays matching documents with title and description
- **Pagination** - Navigate through results

## Customization

Edit `app/components/SearchBox.tsx` to:

- Change the fields being searched in `additionalSearchParameters.query_by`
- Modify the `Hit` component to display different document fields
- Add filters, facets, or sorting widgets from react-instantsearch

### Example: Add a field to results

```tsx
function Hit({ hit }: any) {
  return (
    <article className="border rounded-lg p-4 hover:shadow-lg transition">
      <h2 className="text-lg font-semibold mb-2">{hit.title}</h2>
      <p className="text-gray-600">{hit.description}</p>
      <p className="text-sm text-gray-500 mt-2">ID: {hit.id}</p>
    </article>
  );
}
```

## Running Your App

```bash
npm run dev
```

Visit `http://localhost:3000` to see the search interface.

## Troubleshooting

If you get connection errors:

1. Verify your Typesense server is running on the configured host and port
2. Check the API key is correct
3. Ensure the collection name exists in Typesense
4. Check browser console for CORS or connection errors

## Documentation

- [InstantSearch.js Docs](https://www.algolia.com/doc/api-reference/widgets/js/)
- [Typesense InstantSearch Adapter](https://github.com/typesense/typesense-instantsearch-adapter)
- [React InstantSearch Docs](https://www.algolia.com/doc/guides/building-search-ui/packages/react-instantsearch/react/)
