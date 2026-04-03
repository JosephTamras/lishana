"use client";

import { BaseHit } from "instantsearch.js";
import React from "react";
import { Highlight } from "react-instantsearch";

interface Sense {
  glosses: string;
}

export const HitComponent: React.FC<BaseHit> = ({ hit }) => {
  return (
    <div className="border-b border-slate-200 dark:border-slate-700">
      <div className="px-3 sm:px-4 py-4 sm:py-5">
        <h2 className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-slate-50 font-syriac mb-2 break-words">
          <Highlight hit={hit} attribute="canonical_form" />
        </h2>
        <h3 className="text-sm sm:text-base font-semibold text-slate-600 dark:text-slate-400 font-syriac mb-3 break-words">
          <Highlight hit={hit} attribute="canonical_phonetic" highlightedTagName="mark" />
        </h3>
        <ul className="list-disc list-inside space-y-1 text-sm sm:text-base">
          {(hit.senses as Sense[]).map((_sense: Sense, index: number) => (
            <li
              key={index}
              className="text-slate-700 dark:text-slate-300 font-syriac break-words"
            >
              <Highlight
                hit={hit}
                attribute={`senses.${index}.glosses`}
                highlightedTagName="mark"
              />
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};