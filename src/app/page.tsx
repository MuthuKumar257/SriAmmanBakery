"use client";

import React, { useEffect, useRef, useState, useCallback } from "react";
import { Header } from "@/components/Header";
import { IntroFilm } from "@/components/IntroFilm";
import { HeroSection } from "@/components/HeroSection";
import { CraftRitualSection } from "@/components/CraftRitualSection";
import { SignatureSweetsSection } from "@/components/SignatureSweetsSection";
import { SweetsShowcase } from "@/components/SweetsShowcase";
import { PackSection } from "@/components/PackSection";
import { EstateSection } from "@/components/EstateSection";
import { Footer } from "@/components/Footer";
import { OrderModal } from "@/components/OrderModal";
import { prefersReducedMotion, norm } from "@/lib/utils";

export default function Home() {
  const heroRef = useRef<HTMLElement>(null);
  const slotRef = useRef<HTMLDivElement>(null);

  const [introState, setIntroState] = useState<"playing" | "revealing" | "done">("playing");
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [selectedProduct, setSelectedProduct] = useState<string | undefined>(undefined);

  // Initialize intro state with reduced-motion check
  useEffect(() => {
    if (prefersReducedMotion()) {
      setIntroState("done");
    }
  }, []);

  const handleRevealIntro = useCallback(() => {
    setIntroState((s) => (s === "playing" ? "revealing" : s));
  }, []);

  const handleDoneIntro = useCallback(() => {
    setIntroState("done");
  }, []);

  const isIntroDoneOrRevealing = introState !== "playing";

  // Lock scroll while intro is playing
  useEffect(() => {
    if (!isIntroDoneOrRevealing) {
      document.documentElement.style.overflow = "hidden";
      return () => {
        document.documentElement.style.overflow = "";
        window.dispatchEvent(new Event("resize"));
      };
    }
  }, [isIntroDoneOrRevealing]);

  // Smooth hero fade as user scrolls
  useEffect(() => {
    const handleScroll = () => {
      const hero = heroRef.current;
      if (!hero) return;
      const scrollY = window.scrollY;
      const vh = window.innerHeight;
      const fadeProgress = norm(scrollY / vh, 0.05, 0.6);
      hero.style.setProperty("--hero-fade", String(1 - fadeProgress));
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const handleOpenOrder = (prodName?: string) => {
    setSelectedProduct(prodName);
    setIsModalOpen(true);
  };

  return (
    <div data-intro={isIntroDoneOrRevealing ? "done" : "playing"}>
      {/* Header Navigation */}
      <Header
        logoVisible={introState === "done"}
        linksVisible={isIntroDoneOrRevealing}
        onOpenCatalogue={() => handleOpenOrder()}
      />

      {/* Main Page Sections */}
      <main>
        {/* Section 1: Hero */}
        <HeroSection
          heroRef={heroRef}
          slotRef={slotRef}
          active={isIntroDoneOrRevealing}
        />

        {/* Section 2: The Craft Ritual (Sweet Tray for Ghee, Roast, Craft, Garnish · 01 / 04) */}
        <CraftRitualSection onOpenOrder={handleOpenOrder} />

        {/* Section 3: Luxury Signature Sweets Collection with Iris Aperture & Stacking Scroll */}
        <SignatureSweetsSection
          onSelectSweet={(sweet) => handleOpenOrder(sweet.name)}
        />

        {/* Section 4: Signature 12 Sweets Showcase (Consistent Balanced Responsive Grid) */}
        <SweetsShowcase onOpenDetails={(prod) => handleOpenOrder(prod)} />

        {/* Section 4: The Box / Pack (Falling Garnishes Physics Animation) */}
        <PackSection onOpenOrder={handleOpenOrder} />

        {/* Section 5: Our Story & Heritage Craft (Expanding Arched Reveal & Rotating Seal) */}
        <EstateSection />
      </main>

      {/* Footer */}
      <Footer onOpenOrder={handleOpenOrder} />

      {/* Cinematic Intro Film */}
      {introState !== "done" && (
        <IntroFilm onReveal={handleRevealIntro} onDone={handleDoneIntro} />
      )}

      {/* Interactive Sweets Detail Modal */}
      <OrderModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        initialProduct={selectedProduct}
      />
    </div>
  );
}
