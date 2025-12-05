"use client";
import TypesenseInstantSearchAdapter from "typesense-instantsearch-adapter";
import { singleIndex } from "instantsearch.js/es/lib/stateMappings";
import {
  InstantSearch,
  InfiniteHits,
  Configure,
  useSearchBox,
} from "react-instantsearch";
import React from "react";
import { useSearchParams } from "next/navigation";

const typesenseInstantsearchAdapter = new TypesenseInstantSearchAdapter({
  server: {
    apiKey: process.env.NEXT_PUBLIC_TYPESENSE_API_KEY || "", // Be sure to use the search-only-api-key
    nodes: [
      {
        host: "localhost",
        port: 8108,
        protocol: "http",
      },
    ],
  },
  additionalSearchParameters: {
    query_by: "senses.glosses, forms.form, forms.roman, word",
  },
});

interface Hit {
  word: string;
  senses: Array<any>;
  canonical: string;
}

interface HitComponentProps {
  hit: Hit;
}

// const ExtractCanonical = (): string => {
//   if (hit.forms) {
//     for (const form of hit.forms) {
//       if () {
//   }

const SimplifiedHit = (hit: any) =>{
  return {
    word: hit.word,
    senses: hit.senses,
    // take the form whose tags has "canonical"
    canonical: hit.forms.find((form: any) => form.tags.includes("canonical"))?.form || hit.word,
  } as Hit;
}

const HitComponent: React.FC<HitComponentProps> = ({ hit }) => {
  const simplifiedHit = SimplifiedHit(hit);
  return (<div className="p-4 border-b">
    {/* fallback to lemma if no canonical */}
    <h2 className="text-xl font-bold text-black">{simplifiedHit.canonical}</h2>
    {/* map through senses and have a bullet for each gloss in senses.glosses */}
    <ul className="list-disc list-inside mt-2">
      {simplifiedHit.senses.map((sense, index) => (
        <li key={index} className="text-gray-700">
          {sense.glosses.join(", ")}
        </li>
      ))}
    </ul>
    {/* don't render examples if they are not available, also render all examples*/}
    {/* {hit.examples_english && hit.examples_english.length > 0 && (
      <div className="mt-2">
        <h3 className="font-semibold text-black">Examples:</h3>
        <ul className="list-disc list-inside">
          {hit.examples_english.map((example, index) => (
            <li key={index} className="text-gray-600">
              {example} {hit.examples_syriac && hit.examples_syriac[index] ? ` - ܐܘ ܣܘܪܝܬ: ${hit.examples_syriac[index]}` : ""}
            </li>
          ))}
        </ul>
      </div>
    )} */}
    {/* <p className="text-gray-500 italic">Forms: {hit.forms}</p>
    <p className="text-gray-500 italic">Romanizations: {hit.romanizations}</p> */}
  </div>)
};

const SearchBoxComponent: React.FC = () => {
  const { query, refine } = useSearchBox();

  return (
    <div>
      <input
        type="text"
        name="search-word"
        value={query}
        onChange={(e) => refine(e.target.value)}
        placeholder="Search in English or ܣܘܪܝܬ"
        className="w-full p-2 border border-gray-300 rounded text-black"
      />
    </div>
  );
};

export default function Home() {
  const searchParams = useSearchParams();
  const indexName = "assyrian_dictionary";

  return (
    <div className="flex justify-center items-center flex-col min-h-screen py-2 bg-white">
      <h1 className="text-3xl font-semibold mb-8 text-black">
        Assyrian-English Dictionary
      </h1>
      <InstantSearch
        indexName={indexName}
        searchClient={typesenseInstantsearchAdapter.searchClient}
        routing={{ stateMapping: singleIndex(indexName) }}
        // key={(searchParams.get("query") as string) || ""}
      >
        <Configure hitsPerPage={10} />
        <div className="flex flex-col w-full max-w-xl px-4">
          <SearchBoxComponent />
          <InfiniteHits hitComponent={HitComponent} showPrevious={false} classNames={{
            loadMore: "text-black"
          }} />
        </div>
      </InstantSearch>
    </div>
  );
}