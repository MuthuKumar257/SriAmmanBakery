"use client";

import React from "react";
import Image from "next/image";
import { siteConfig } from "@/config/site";

interface FooterProps {
  onOpenOrder: (productName?: string) => void;
}

export const Footer: React.FC<FooterProps> = ({ onOpenOrder }) => {
  const sectionTitleClass =
    "mb-5 text-[.66rem] font-normal tracking-[.3em] text-[#C99732] uppercase";
  const linkClass = "text-[#F7F1E5]/80 transition-colors duration-300 hover:text-[#C99732]";

  return (
    <footer className="footer-bg relative px-(--pad) pt-[clamp(56px,10vh,110px)] pb-7 text-[#F7F1E5]">
      <div className="grid grid-cols-[minmax(0,1.5fr)_minmax(0,1fr)_minmax(0,1fr)] gap-x-10 gap-y-12 max-[860px]:grid-cols-2">
        {/* Brand Column */}
        <div className="max-[860px]:col-span-2">
          {/* Logo in original colors per Rule 5 */}
          <Image
            src="/logo.png"
            alt={siteConfig.brandName}
            width={862}
            height={688}
            className="-ml-4 block h-[clamp(120px,18vh,170px)] w-auto object-contain"
          />
          <p className="mt-5 max-w-[32ch] text-[clamp(.9rem,1.05vw,1.05rem)] text-[#F7F1E5]/80 leading-relaxed">
            {siteConfig.footer.description}
          </p>

          <div className="mt-6 flex items-center gap-3">
            <button
              type="button"
              onClick={() => onOpenOrder()}
              className="inline-flex cursor-pointer items-center gap-2 rounded-full border border-[#C99732]/45 bg-[#123D32] px-5 py-2.5 text-[.68rem] font-medium tracking-[.22em] text-[#C99732] uppercase shadow-sm transition-all hover:bg-[#C99732] hover:text-[#0A241E]"
            >
              View Sweets Collection
            </button>
          </div>
        </div>

        {/* Explore Links */}
        <nav aria-label="Footer Section Navigation">
          <p className={sectionTitleClass}>Explore</p>
          <ul className="grid gap-3 font-serif text-[clamp(1.25rem,1.7vw,1.6rem)] leading-tight">
            {siteConfig.navLinks.map(({ id, label }) => (
              <li key={id}>
                <a href={`#${id}`} className={linkClass}>
                  {label}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        {/* Collection & Specialties */}
        <div>
          <p className={sectionTitleClass}>The Collection</p>
          <ul className="grid gap-2 text-[clamp(.9rem,1.05vw,1.05rem)] text-[#F7F1E5]/80">
            {siteConfig.catalogue.map((sweet) => (
              <li key={sweet.id}>
                <button
                  type="button"
                  onClick={() => onOpenOrder(sweet.name)}
                  className="cursor-pointer text-left transition-colors duration-300 hover:text-[#C99732]"
                >
                  {sweet.name}
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="mt-[clamp(44px,8vh,84px)] flex flex-wrap items-center justify-between gap-x-8 gap-y-3 border-t border-[#C99732]/20 pt-6 text-[.66rem] font-normal tracking-[.22em] text-[#F7F1E5]/60 uppercase">
        <p>{siteConfig.footer.copyright}</p>
        <div className="flex items-center gap-6">
          <span className="text-[#F7F1E5]/45">{siteConfig.location}</span>
          <a
            href="#top"
            className="text-[#C99732] transition-colors duration-300 hover:text-[#F7F1E5]"
          >
            Back to top ↑
          </a>
        </div>
      </div>
    </footer>
  );
};
