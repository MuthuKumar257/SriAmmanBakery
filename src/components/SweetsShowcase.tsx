"use client";

import React, { useState } from "react";
import Image from "next/image";
import { siteConfig } from "@/config/site";
import { Sparkles, ArrowRight, Check } from "lucide-react";

interface SweetsShowcaseProps {
  onOpenDetails: (productName: string) => void;
}

export const SweetsShowcase: React.FC<SweetsShowcaseProps> = ({ onOpenDetails }) => {
  const [imageErrors, setImageErrors] = useState<Record<string, boolean>>({});

  return (
    <section
      id="sweets"
      data-tone="light"
      className="relative min-h-screen bg-[#F7F1E5] px-(--pad) py-[clamp(64px,11vh,128px)] text-[#123D32] overflow-hidden"
    >
      {/* Subtle Warm Heritage Gold Ambient Background */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(ellipse_70%_50%_at_50%_15%,rgba(201,151,50,0.12),transparent_75%)]"
      />

      {/* Section Header */}
      <div className="mx-auto max-w-4xl text-center">
        <p className="flex items-center justify-center gap-4 text-[.72rem] font-medium tracking-[.28em] text-[#651B24] uppercase before:h-px before:w-12 before:bg-[#C99732]/60 after:h-px after:w-12 after:bg-[#C99732]/60">
          <Sparkles className="size-3.5 text-[#C99732]" />
          <span>{siteConfig.taglineWording}</span>
        </p>

        <h2 className="mt-3 font-serif text-[clamp(2.4rem,5.2vw,4.8rem)] leading-[1.04] font-medium tracking-[-.015em] text-[#123D32]">
          Our Signature{" "}
          <em className="font-normal italic text-[#651B24]">
            Sweets Collection.
          </em>
        </h2>

        <p className="mx-auto mt-4 max-w-2xl text-[clamp(.9rem,1.1vw,1.08rem)] leading-relaxed text-[#123D32]/80">
          Handcrafted daily with 100% pure homemade ghee, authentic roasted malts, and natural ingredients.
          Twelve traditional specialties prepared with care and devotion.
        </p>
      </div>

      {/* Responsive 12-Sweet Grid: 4 per row on XL, 3 on LG, 2 on SM, 1 on Mobile */}
      <div className="mx-auto mt-[clamp(44px,7vh,80px)] grid max-w-7xl grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 lg:gap-8">
        {siteConfig.sweets.map((sweet, index) => {
          const hasError = imageErrors[sweet.id];
          const fallbackSrc = `/garnishes/${(index % 7) + 1}.png`;

          return (
            <div
              key={sweet.id}
              role="button"
              tabIndex={0}
              onClick={() => onOpenDetails(sweet.name)}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  onOpenDetails(sweet.name);
                }
              }}
              aria-label={`View details of ${sweet.name}`}
              className="group relative flex w-full cursor-pointer flex-col justify-between overflow-hidden rounded-2xl border border-[#C99732]/35 bg-[#FFFFFF] p-5 shadow-[0_12px_30px_rgba(18,61,50,0.06)] transition-all duration-500 hover:-translate-y-1.5 hover:border-[#C99732] hover:bg-[#FFFDF9] hover:shadow-[0_22px_48px_rgba(18,61,50,0.14)] focus-visible:outline-2 focus-visible:outline-[#C99732]"
            >
              {/* Top Details & Fixed Height Image Container */}
              <div className="flex flex-col flex-1">
                {/* Image Container with Consistent 4:3 Aspect Ratio (Pristine Natural Photos per Rule 7) */}
                <div className="relative aspect-[4/3] w-full overflow-hidden rounded-xl bg-[#FAF6EF]">
                  <Image
                    src={hasError ? fallbackSrc : sweet.image}
                    alt={`${sweet.name} - ${siteConfig.brandName}`}
                    fill
                    sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, (max-width: 1280px) 33vw, 25vw"
                    className="h-full w-full object-cover transition-transform duration-700 ease-[cubic-bezier(.22,.7,.2,1)] group-hover:scale-105"
                    onError={() =>
                      setImageErrors((prev) => ({ ...prev, [sweet.id]: true }))
                    }
                  />

                  {/* Subtle Gradient Overlay */}
                  <div className="absolute inset-0 bg-gradient-to-t from-[#123D32]/60 via-transparent to-transparent opacity-40 transition-opacity duration-300 group-hover:opacity-20" />

                  {/* Deep Maroon Badge with Heritage Gold Border */}
                  {sweet.badge && (
                    <span className="absolute top-3 right-3 rounded-full border border-[#C99732]/50 bg-[#651B24]/90 px-3 py-1 text-[.64rem] font-medium tracking-wider text-[#F7F1E5] uppercase backdrop-blur-md shadow-sm">
                      {sweet.badge}
                    </span>
                  )}

                  {/* Category Pill */}
                  <span className="absolute bottom-3 left-3 rounded-md bg-[#123D32]/80 px-2.5 py-0.5 text-[.64rem] font-normal tracking-[.2em] text-[#F7F1E5] uppercase backdrop-blur-sm">
                    {sweet.category}
                  </span>
                </div>

                {/* Sweet Title & Subtitle (with subtitle support for Milk Laddu) */}
                <div className="mt-5 flex items-start justify-between border-b border-[#C99732]/20 pb-3 min-h-[4rem]">
                  <div className="pr-2">
                    <h3 className="font-serif text-2xl font-medium tracking-tight text-[#651B24] transition-colors duration-300 group-hover:text-[#123D32]">
                      {sweet.name}
                    </h3>
                    {sweet.subtitle && (
                      <p className="mt-0.5 text-[.74rem] font-normal tracking-wide text-[#123D32]/80 italic">
                        {sweet.subtitle}
                      </p>
                    )}
                  </div>
                  <span className="text-[.68rem] tracking-wider text-[#C99732] uppercase font-medium shrink-0 pt-1">
                    Traditional
                  </span>
                </div>

                {/* Description with consistent height & clamp */}
                <p className="mt-3 text-[.86rem] leading-relaxed text-[#123D32]/85 line-clamp-3 min-h-[3.9rem]">
                  {sweet.description}
                </p>

                {/* Key Ingredients */}
                <div className="mt-4 flex flex-wrap gap-1.5 min-h-[1.75rem]">
                  {sweet.ingredients.slice(0, 3).map((ing) => (
                    <span
                      key={ing}
                      className="rounded-full border border-[#123D32]/12 bg-[#123D32]/8 px-2.5 py-0.5 text-[.66rem] font-medium text-[#123D32]"
                    >
                      {ing}
                    </span>
                  ))}
                  {sweet.ingredients.length > 3 && (
                    <span className="rounded-full bg-[#123D32]/5 px-2 py-0.5 text-[.66rem] text-[#123D32]/60">
                      +{sweet.ingredients.length - 3} more
                    </span>
                  )}
                </div>
              </div>

              {/* Informational Card Footer (Clickable Action Prompt) */}
              <div className="mt-6 flex items-center justify-between border-t border-[#C99732]/20 pt-4 text-[.72rem] font-medium tracking-wider text-[#123D32] uppercase transition-colors duration-300 group-hover:text-[#651B24]">
                <span>View Sweet Profile</span>
                <ArrowRight className="size-4 text-[#C99732] transition-transform duration-300 group-hover:translate-x-1" />
              </div>
            </div>
          );
        })}
      </div>

      {/* Freshness Assurance Bar - Deep Forest Green Background */}
      <div className="mx-auto mt-16 max-w-4xl rounded-2xl border border-[#C99732]/35 bg-[#123D32] p-6 text-center shadow-lg">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3 text-xs text-[#F7F1E5]">
          <div className="flex items-center justify-center gap-2">
            <Check className="size-4 text-[#C99732]" />
            <span className="font-medium tracking-wide">100% Pure Homemade Ghee</span>
          </div>
          <div className="flex items-center justify-center gap-2 border-y border-[#C99732]/25 py-2 sm:border-y-0 sm:border-x sm:py-0">
            <Check className="size-4 text-[#C99732]" />
            <span className="font-medium tracking-wide">Baked & Prepared Fresh Daily</span>
          </div>
          <div className="flex items-center justify-center gap-2">
            <Check className="size-4 text-[#C99732]" />
            <span className="font-medium tracking-wide">Authentic Boost & Horlicks Malts</span>
          </div>
        </div>
      </div>
    </section>
  );
};
