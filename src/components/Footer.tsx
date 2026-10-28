"use client";

import React from "react";
import Image from "next/image";
import { siteConfig } from "@/config/site";
import { Instagram, Phone, MessageCircle, ExternalLink } from "lucide-react";

interface FooterProps {
  onOpenOrder: (productName?: string) => void;
}

export const Footer: React.FC<FooterProps> = ({ onOpenOrder }) => {
  const sectionTitleClass =
    "mb-5 text-[.66rem] font-medium tracking-[.3em] text-[#C99732] uppercase";
  const linkClass =
    "text-[#F7F1E5]/80 transition-colors duration-300 hover:text-[#C99732]";

  return (
    <footer className="footer-bg relative px-(--pad) pt-[clamp(56px,10vh,110px)] pb-7 text-[#F7F1E5]">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-x-10 gap-y-12">
        {/* Brand Column */}
        <div className="lg:col-span-1 md:col-span-2">
          {/* Logo in original colors per Rule 5 */}
          <Image
            src="/logo.png"
            alt={siteConfig.brandName}
            width={862}
            height={688}
            className="-ml-4 block h-[clamp(110px,16vh,160px)] w-auto object-contain"
          />
          <p className="mt-4 max-w-[32ch] text-[clamp(.88rem,1vw,1rem)] text-[#F7F1E5]/80 leading-relaxed">
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
          <ul className="grid gap-3 font-serif text-[clamp(1.2rem,1.5vw,1.5rem)] leading-tight">
            {siteConfig.navLinks.map(({ id, label }) => (
              <li key={id}>
                <a href={`#${id}`} className={linkClass}>
                  {label}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        {/* Contact & Connect Details */}
        <div>
          <p className={sectionTitleClass}>Contact & Connect</p>
          <ul className="grid gap-4 text-[clamp(.85rem,.95vw,.95rem)] text-[#F7F1E5]/85">
            {/* Phone */}
            <li>
              <a
                href={`tel:${siteConfig.footer.phone}`}
                className="group flex items-start gap-3 transition-colors duration-300 hover:text-[#C99732]"
              >
                <span className="flex size-9 shrink-0 items-center justify-center rounded-full border border-[#C99732]/35 bg-[#0A241E]/80 text-[#C99732] transition-all duration-300 group-hover:border-[#C99732] group-hover:bg-[#C99732] group-hover:text-[#0A241E]">
                  <Phone className="size-4" />
                </span>
                <div>
                  <span className="block text-[.64rem] font-semibold tracking-wider text-[#C99732] uppercase">
                    Call Us
                  </span>
                  <span className="font-medium tracking-wide">
                    {siteConfig.footer.phoneDisplay}
                  </span>
                </div>
              </a>
            </li>

            {/* Instagram */}
            <li>
              <a
                href={siteConfig.footer.instagram}
                target="_blank"
                rel="noopener noreferrer"
                className="group flex items-start gap-3 transition-colors duration-300 hover:text-[#C99732]"
              >
                <span className="flex size-9 shrink-0 items-center justify-center rounded-full border border-[#C99732]/35 bg-[#0A241E]/80 text-[#C99732] transition-all duration-300 group-hover:border-[#C99732] group-hover:bg-[#C99732] group-hover:text-[#0A241E]">
                  <Instagram className="size-4" />
                </span>
                <div>
                  <span className="block text-[.64rem] font-semibold tracking-wider text-[#C99732] uppercase">
                    Instagram
                  </span>
                  <span className="font-medium tracking-wide inline-flex items-center gap-1">
                    @sriamman_bakery
                    <ExternalLink className="size-3 opacity-60" />
                  </span>
                </div>
              </a>
            </li>

            {/* WhatsApp Community Channel */}
            <li>
              <a
                href={siteConfig.footer.whatsappChannel}
                target="_blank"
                rel="noopener noreferrer"
                className="group flex items-start gap-3 transition-colors duration-300 hover:text-[#C99732]"
              >
                <span className="flex size-9 shrink-0 items-center justify-center rounded-full border border-[#C99732]/35 bg-[#0A241E]/80 text-[#C99732] transition-all duration-300 group-hover:border-[#C99732] group-hover:bg-[#C99732] group-hover:text-[#0A241E]">
                  <MessageCircle className="size-4" />
                </span>
                <div>
                  <span className="block text-[.64rem] font-semibold tracking-wider text-[#C99732] uppercase">
                    WhatsApp Channel
                  </span>
                  <span className="font-medium tracking-wide inline-flex items-center gap-1">
                    Join Updates Channel
                    <ExternalLink className="size-3 opacity-60" />
                  </span>
                </div>
              </a>
            </li>
          </ul>
        </div>

        {/* Collection & Specialties */}
        <div>
          <p className={sectionTitleClass}>The Collection</p>
          <ul className="grid grid-cols-2 gap-x-4 gap-y-2 text-[clamp(.84rem,.95vw,.95rem)] text-[#F7F1E5]/80">
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
