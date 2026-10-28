"use client";

import React, { useEffect, useState } from "react";
import Image from "next/image";
import { siteConfig, SweetProduct } from "@/config/site";
import { X, Sparkles, Check } from "lucide-react";

interface OrderModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialProduct?: string;
}

export const OrderModal: React.FC<OrderModalProps> = ({
  isOpen,
  onClose,
  initialProduct,
}) => {
  const [selectedSweet, setSelectedSweet] = useState<SweetProduct>(
    siteConfig.catalogue[0]
  );
  const [imgError, setImgError] = useState<boolean>(false);

  useEffect(() => {
    if (initialProduct) {
      const match = siteConfig.catalogue.find(
        (p) => p.name.toLowerCase() === initialProduct.toLowerCase()
      );
      if (match) setSelectedSweet(match);
    } else {
      setSelectedSweet(siteConfig.catalogue[0]);
    }
    setImgError(false);
  }, [initialProduct, isOpen]);

  // Handle ESC key press and scroll locking
  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onClose();
      }
    };

    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = originalOverflow;
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="sweet-modal-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6"
    >
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-[#0A241E]/88 backdrop-blur-md transition-opacity duration-300 animate-fade-in"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Modal Dialog Card */}
      <div className="relative z-10 flex max-h-[92vh] w-full max-w-3xl flex-col overflow-hidden rounded-2xl border border-[#C99732]/45 bg-[#0D2D25] shadow-[0_30px_70px_-15px_rgba(7,27,22,0.95)] text-[#F7F1E5] animate-rise">
        {/* Top Header Bar */}
        <div className="flex items-center justify-between border-b border-[#C99732]/25 px-6 py-4 bg-[#09221C]">
          <div className="flex items-center gap-2.5 text-[.7rem] font-medium tracking-[.26em] text-[#C99732] uppercase">
            <Sparkles className="size-3.5 text-[#C99732]" />
            <span>{siteConfig.brandName} · Sweet Profile</span>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="cursor-pointer rounded-full p-2 text-[#C99732]/80 transition-all duration-200 hover:bg-[#C99732]/15 hover:text-[#F7F1E5] focus-visible:outline-2 focus-visible:outline-[#C99732]"
            aria-label="Close sweet description"
          >
            <X className="size-5" />
          </button>
        </div>

        {/* Modal Scrollable Body */}
        <div className="overflow-y-auto px-6 py-6 sm:px-8">
          {/* Quick Sweets Selector Tabs */}
          <div className="mb-6">
            <p className="text-[.66rem] font-medium tracking-[.24em] text-[#C99732]/85 uppercase">
              Featured Sweets Collection
            </p>
            <div className="mt-2.5 flex flex-wrap gap-2">
              {siteConfig.catalogue.map((sweet) => {
                const isActive = sweet.id === selectedSweet.id;
                return (
                  <button
                    key={sweet.id}
                    type="button"
                    onClick={() => {
                      setSelectedSweet(sweet);
                      setImgError(false);
                    }}
                    className={`cursor-pointer rounded-full px-3.5 py-1 text-[.7rem] font-medium tracking-wider uppercase transition-all duration-200 ${
                      isActive
                        ? "border border-[#C99732] bg-[#C99732] text-[#0A241E] shadow-[0_4px_12px_rgba(201,151,50,0.35)]"
                        : "border border-[#C99732]/30 bg-[#123D32]/80 text-[#F7F1E5]/80 hover:border-[#C99732]/60 hover:text-[#F7F1E5]"
                    }`}
                  >
                    {sweet.name}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Main Sweet Showcase Grid */}
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 sm:gap-8">
            {/* Photograph Container (Natural & Realistic per Rule 7) */}
            <div className="relative aspect-[4/3] w-full overflow-hidden rounded-xl border border-[#C99732]/35 bg-[#09221C] shadow-inner sm:aspect-square">
              <Image
                src={imgError ? "/sweet.png" : selectedSweet.image}
                alt={`${selectedSweet.name} - ${siteConfig.brandName}`}
                fill
                sizes="(max-width: 640px) 100vw, 400px"
                className="h-full w-full object-cover transition-transform duration-500 hover:scale-105"
                onError={() => setImgError(true)}
              />

              {/* Deep Maroon Badge with Gold Border */}
              {selectedSweet.badge && (
                <span className="absolute top-3 right-3 rounded-full border border-[#C99732]/50 bg-[#651B24]/90 px-3 py-1 text-[.64rem] font-medium tracking-wider text-[#F7F1E5] uppercase backdrop-blur-md">
                  {selectedSweet.badge}
                </span>
              )}

              {/* Category */}
              <span className="absolute bottom-3 left-3 rounded-md bg-[#0A241E]/85 px-2.5 py-1 text-[.64rem] font-normal tracking-[.2em] text-[#F7F1E5]/90 uppercase backdrop-blur-sm">
                {selectedSweet.category}
              </span>
            </div>

            {/* Sweet Descriptions & Ingredients */}
            <div className="flex flex-col justify-between">
              <div>
                <h2
                  id="sweet-modal-title"
                  className="font-serif text-[clamp(2rem,3.2vw,2.75rem)] leading-none font-medium text-[#F7F1E5]"
                >
                  {selectedSweet.name}
                </h2>

                {selectedSweet.subtitle && (
                  <p className="mt-1.5 text-[.82rem] font-normal tracking-wide text-[#C99732] italic">
                    {selectedSweet.subtitle}
                  </p>
                )}

                <p className="mt-3 text-[.9rem] leading-relaxed text-[#F7F1E5]/80">
                  {selectedSweet.description}
                </p>

                {/* Taste & Texture Profile */}
                <div className="mt-4 rounded-xl border border-[#C99732]/25 bg-[#09221C]/80 p-4">
                  <h3 className="text-[.68rem] font-medium tracking-[.22em] text-[#C99732] uppercase">
                    Taste & Texture
                  </h3>
                  <p className="mt-1.5 text-[.84rem] leading-relaxed text-[#F7F1E5]/90">
                    {selectedSweet.tasteAndTexture}
                  </p>
                </div>

                {/* Ingredients List */}
                <div className="mt-4">
                  <h3 className="text-[.68rem] font-medium tracking-[.22em] text-[#C99732]/85 uppercase">
                    Authentic Ingredients
                  </h3>
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {selectedSweet.ingredients.map((ing) => (
                      <span
                        key={ing}
                        className="rounded-full border border-[#C99732]/30 bg-[#123D32] px-3 py-1 text-[.68rem] text-[#C99732]"
                      >
                        {ing}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Freshness & Quality Assurance */}
              <div className="mt-6 flex flex-wrap items-center justify-between gap-3 border-t border-[#C99732]/25 pt-4 text-[.74rem] text-[#F7F1E5]/80">
                <div className="flex items-center gap-1.5">
                  <Check className="size-4 text-[#C99732]" />
                  <span>100% Pure Homemade Ghee</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Check className="size-4 text-[#C99732]" />
                  <span>Shelf Life: {selectedSweet.shelfLife}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Modal Bottom Footer */}
        <div className="flex items-center justify-between border-t border-[#C99732]/25 bg-[#09221C] px-6 py-4">
          <span className="text-[.68rem] font-normal tracking-[.22em] text-[#C99732]/80 uppercase">
            Serving sweetness since 2022
          </span>
          <button
            type="button"
            onClick={onClose}
            className="cursor-pointer rounded-full bg-[#C99732] px-6 py-2 text-[.72rem] font-medium tracking-wider text-[#0A241E] uppercase transition-all duration-300 hover:bg-[#F7F1E5] hover:shadow-[0_4px_16px_rgba(201,151,50,0.4)]"
          >
            Back to Sweets Collection
          </button>
        </div>
      </div>
    </div>
  );
};

export const SweetDetailModal = OrderModal;
