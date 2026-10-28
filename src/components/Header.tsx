"use client";

import React, { useEffect, useRef, useState } from "react";
import Image from "next/image";
import { siteConfig } from "@/config/site";

interface HeaderProps {
  logoVisible: boolean;
  linksVisible: boolean;
  onOpenCatalogue?: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  logoVisible,
  linksVisible,
  onOpenCatalogue,
}) => {
  const headerRef = useRef<HTMLElement>(null);
  const [activeSection, setActiveSection] = useState<string>("");

  useEffect(() => {
    const headerEl = headerRef.current;
    if (!headerEl) return;

    const handleScroll = () => {
      const mid = headerEl.offsetHeight / 2;
      // Check if header is over a light-toned section (e.g. #sweets or #pack)
      const lightSections = Array.from(
        document.querySelectorAll('section[data-tone="light"]')
      );
      const isOverLight = lightSections.some((sec) => {
        const rect = sec.getBoundingClientRect();
        return rect.top <= mid && rect.bottom > mid;
      });

      headerEl.dataset.tone = isOverLight ? "light" : "dark";

      // Detect active navigation section
      const viewMid = window.innerHeight / 2;
      const current = siteConfig.navLinks.find(({ id }) => {
        const target = document.getElementById(id);
        if (!target) return false;
        const rect = target.getBoundingClientRect();
        return rect.top <= viewMid && rect.bottom > viewMid;
      });

      setActiveSection(current?.id ?? "");
    };

    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });
    window.addEventListener("resize", handleScroll);

    return () => {
      window.removeEventListener("scroll", handleScroll);
      window.removeEventListener("resize", handleScroll);
    };
  }, []);

  const navItemClass = [
    "rounded-full border border-transparent px-4 py-2 text-[#F7F1E5]/75 transition-colors duration-500 hover:text-[#C99732] max-[860px]:px-2.5",
    "data-[active=true]:border-[#C99732]/60 data-[active=true]:bg-[#C99732]/15 data-[active=true]:text-[#F7F1E5]",
    "group-data-[tone=light]:text-[#123D32]/85 group-data-[tone=light]:hover:text-[#651B24]",
    "group-data-[tone=light]:data-[active=true]:border-[#123D32]/50 group-data-[tone=light]:data-[active=true]:bg-[#123D32]/12 group-data-[tone=light]:data-[active=true]:text-[#651B24]",
  ].join(" ");

  return (
    <header
      ref={headerRef}
      className="group fixed inset-x-0 top-0 z-30 flex items-center justify-between px-(--pad) py-[clamp(8px,1.4vh,16px)] text-[.72rem] font-normal tracking-[.26em] uppercase"
    >
      {/* Brand Nav Logo - Retains original colors per Rule 5 */}
      <a
        href="#top"
        aria-label={`${siteConfig.brandName}, back to top`}
        className="-ml-2.5 block focus-visible:outline-2 focus-visible:outline-[#C99732]"
      >
        <Image
          src="/logo.png"
          alt={siteConfig.brandName}
          width={862}
          height={688}
          data-nav-logo=""
          priority
          className={`block h-[clamp(54px,9vh,80px)] w-auto transition-opacity duration-500 ${
            logoVisible ? "opacity-100" : "opacity-0"
          }`}
        />
      </a>

      {/* Navigation Links - Forest green navigation styling with gold and maroon accents */}
      <nav
        aria-label="Main Navigation"
        className={`-mr-4 flex items-center gap-1.5 transition-[opacity,translate] delay-500 duration-1000 ease-[cubic-bezier(.22,.7,.2,1)] max-[860px]:-mr-3 max-[860px]:gap-0.5 ${
          linksVisible ? "opacity-100" : "pointer-events-none -translate-y-3 opacity-0"
        }`}
      >
        {siteConfig.navLinks.map(({ id, label, shortLabel }) => (
          <a
            key={id}
            href={`#${id}`}
            data-active={activeSection === id}
            aria-current={activeSection === id ? "true" : undefined}
            className={navItemClass}
          >
            <span className="max-[860px]:hidden">{label}</span>
            <span className="hidden max-[860px]:inline">{shortLabel}</span>
          </a>
        ))}

        {/* Quick Sweets Menu Pill - Primary Deep Forest Green Button */}
        {onOpenCatalogue && (
          <button
            type="button"
            onClick={onOpenCatalogue}
            className="ml-2 cursor-pointer rounded-full border border-[#C99732]/45 bg-[#123D32]/85 px-3.5 py-1.5 text-[.66rem] font-medium tracking-[.2em] text-[#C99732] shadow-sm transition-all hover:bg-[#C99732] hover:text-[#0A241E] group-data-[tone=light]:border-[#123D32]/40 group-data-[tone=light]:bg-[#123D32] group-data-[tone=light]:text-[#F7F1E5] group-data-[tone=light]:hover:bg-[#651B24] max-[860px]:hidden"
          >
            Sweets Collection
          </button>
        )}
      </nav>
    </header>
  );
};
