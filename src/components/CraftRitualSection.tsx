"use client";

import React, { useEffect, useRef, useState } from "react";
import Image from "next/image";
import { siteConfig } from "@/config/site";
import { clamp, easeInOutCubic, lerp, norm, prefersReducedMotion } from "@/lib/utils";
import { Sparkles } from "lucide-react";

interface CraftRitualSectionProps {
  onOpenOrder: (productName?: string) => void;
}

const padZero = (n: number) => String(n).padStart(2, "0");

export const CraftRitualSection: React.FC<CraftRitualSectionProps> = ({ onOpenOrder }) => {
  const sectionRef = useRef<HTMLElement>(null);
  const stageRef = useRef<HTMLDivElement>(null);
  const railRef = useRef<HTMLDivElement>(null);
  const trayRef = useRef<HTMLDivElement>(null);
  const [activeChapter, setActiveChapter] = useState<number>(0);
  const chapters = siteConfig.craftChapters;

  useEffect(() => {
    const sec = sectionRef.current;
    const stage = stageRef.current;
    const rail = railRef.current;
    const tray = trayRef.current;

    if (!sec || !stage || !rail || !tray) return;

    const reduced = prefersReducedMotion();
    let animId = 0;
    let isIntersecting = false;
    let smoothedProgress = 0;
    let lastChapter = 0;
    let lastTime = performance.now();

    const updateFrame = (now: number) => {
      const delta = Math.min((now - lastTime) / 1000, 0.05);
      lastTime = now;

      const vh = window.innerHeight;
      const rect = sec.getBoundingClientRect();
      const rawProgress = clamp(-rect.top / (sec.offsetHeight - vh));

      smoothedProgress = reduced
        ? rawProgress
        : lerp(smoothedProgress, rawProgress, 1 - Math.exp(-delta * 12));

      if (Math.abs(rawProgress - smoothedProgress) < 0.001) {
        smoothedProgress = rawProgress;
      }

      // Update progress on rail track
      rail.style.setProperty("--progress", smoothedProgress.toFixed(4));

      // Parallax & floating tilt for the Sweet Tray
      const p = smoothedProgress;
      const trayScale = reduced ? 1 : lerp(0.96, 1.04, Math.sin(p * Math.PI));
      const trayY = reduced ? 0 : lerp(24, -20, p);
      const trayRotate = reduced ? 0 : lerp(-2.5, 2.5, Math.sin(p * Math.PI * 2));
      tray.style.transform = `translate3d(0, ${trayY}px, 0) scale(${trayScale}) rotate(${trayRotate}deg)`;

      // Determine active chapter (0 to 3)
      let currentChap = 0;
      for (
        let i = 0;
        i < chapters.length - 1 && p >= chapters[i + 1].start;
        i++
      ) {
        currentChap = i + 1;
      }

      if (currentChap !== lastChapter) {
        lastChapter = currentChap;
        setActiveChapter(currentChap);
      }

      if (isIntersecting) {
        animId = requestAnimationFrame(updateFrame);
      }
    };

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !isIntersecting) {
          isIntersecting = true;
          lastTime = performance.now();
          animId = requestAnimationFrame(updateFrame);
        } else if (!entry.isIntersecting) {
          isIntersecting = false;
          cancelAnimationFrame(animId);
        }
      },
      { rootMargin: "20% 0px" }
    );

    observer.observe(sec);
    updateFrame(performance.now());

    return () => {
      isIntersecting = false;
      cancelAnimationFrame(animId);
      observer.disconnect();
    };
  }, [chapters]);

  return (
    <section
      id="craft"
      ref={sectionRef}
      className="relative h-[360vh] bg-[#123D32] text-[#F7F1E5]"
    >
      <div
        ref={stageRef}
        className="sticky top-0 grid h-svh min-h-[540px] grid-cols-[minmax(0,5.2fr)_minmax(0,6.8fr)] items-center overflow-hidden max-[860px]:grid-cols-1 max-[860px]:grid-rows-[auto_auto] max-[860px]:content-center"
      >
        {/* Left Column: Craft Chapters, Progress Rail & 01 / 04 Step Counter */}
        <div className="relative z-10 pl-(--pad) pr-6 max-[860px]:row-start-2 max-[860px]:px-(--pad) max-[860px]:pt-2">
          {/* Section Kicker */}
          <div className="mb-4 flex items-center gap-2.5 text-[.68rem] font-medium tracking-[.28em] text-[#C99732] uppercase">
            <Sparkles className="size-3.5 text-[#C99732]" />
            <span>The Traditional Sweet Ritual</span>
          </div>

          {/* Sequential Chapter Descriptions (Ghee, Roast, Craft, Garnish) */}
          <div className="grid min-h-[160px]">
            {chapters.map((chap, idx) => {
              const state =
                idx === activeChapter
                  ? "active"
                  : idx < activeChapter
                  ? "past"
                  : "ahead";

              return (
                <article
                  key={chap.label}
                  className="chapter"
                  data-state={state}
                  aria-hidden={idx !== activeChapter}
                >
                  <h2 className="font-serif text-[clamp(2.3rem,4.4vw,4.5rem)] leading-[1.02] font-medium tracking-[-.015em] text-balance max-[860px]:text-[clamp(1.8rem,7.5vw,2.6rem)]">
                    {chap.title}{" "}
                    <em className="block font-normal text-[#C99732]">
                      {chap.accent}
                    </em>
                  </h2>

                  <p className="mt-[clamp(14px,2.2vh,24px)] max-w-[38ch] text-[clamp(.92rem,1.1vw,1.1rem)] leading-relaxed text-[#F7F1E5]/80 max-[860px]:mt-2 max-[860px]:text-[.88rem]">
                    {chap.body}
                  </p>
                </article>
              );
            })}
          </div>

          {/* Interactive Step Progress Rail (Ghee · Roast · Craft · Garnish) */}
          <div
            ref={railRef}
            aria-hidden="true"
            className="mt-[clamp(28px,5.5vh,54px)] max-[860px]:mt-5"
          >
            {/* The Rail Track */}
            <div className="rail-track">
              {/* Animated Progress Fill Bar */}
              <span className="rail-fill" />

              {/* Step Dots for Ghee, Roast, Craft, Garnish */}
              {chapters.map((chap, idx) => (
                <i
                  key={chap.label}
                  className="rail-dot"
                  data-active={idx <= activeChapter}
                  style={{
                    left: `calc((100% - 12px) * ${chap.start} + 6px)`,
                  }}
                />
              ))}

              {/* Rolling Mysore Pak / Sweet Garnish Gliding Along the Track */}
              <Image
                src="/garnishes/2.png"
                alt=""
                width={56}
                height={56}
                className="rail-bean pointer-events-none"
              />
            </div>

            {/* Step Labels: Ghee · Roast · Craft · Garnish */}
            <ol className="relative mt-3.5 h-[1.6em] text-[.66rem] font-medium tracking-[.24em] uppercase">
              {chapters.map((chap, idx) => (
                <li
                  key={chap.label}
                  className="rail-step cursor-pointer"
                  data-active={idx <= activeChapter}
                  style={{ left: `${chap.start * 100}%` }}
                >
                  {chap.label}
                </li>
              ))}
            </ol>
          </div>

          {/* Chapter Counter: 01 / 04, 02 / 04, 03 / 04, 04 / 04 */}
          <div className="mt-[clamp(16px,2.8vh,28px)] flex items-center justify-between border-t border-[#C99732]/20 pt-4 max-[860px]:mt-3 max-[860px]:pt-2.5">
            <p className="flex items-baseline gap-2 text-[.74rem] font-normal tracking-[.22em] text-[#F7F1E5]/80 tabular-nums">
              <b className="font-serif text-[clamp(2rem,3.2vw,3rem)] leading-none font-medium tracking-normal text-[#C99732]">
                {padZero(activeChapter + 1)}
              </b>
              <span className="text-base text-[#F7F1E5]/50">/</span>
              <span className="text-sm font-light text-[#F7F1E5]/70">
                {padZero(chapters.length)}
              </span>
            </p>

            {/* Current Step Highlight Badge */}
            <span className="rounded-full border border-[#C99732]/40 bg-[#0A241E]/85 px-3.5 py-1 text-[.66rem] font-medium tracking-wider text-[#C99732] uppercase backdrop-blur-md">
              {chapters[activeChapter].highlight}
            </span>
          </div>
        </div>

        {/* Right Column: Centerpiece Sweet Tray */}
        <div className="relative flex h-full items-center justify-center pr-(--pad) max-[860px]:row-start-1 max-[860px]:h-auto max-[860px]:px-(--pad) max-[860px]:pt-14">
          {/* Subtle Ambient Radial Glow */}
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(ellipse_65%_65%_at_50%_50%,rgba(201,151,50,0.18),transparent_72%)]"
          />

          {/* Sweet Tray Container with Smooth Parallax Float & Tilt */}
          <div
            ref={trayRef}
            className="group relative flex flex-col items-center will-change-transform"
          >
            {/* The Royal Brass Sweet Tray Image */}
            <div className="relative aspect-[13/11] w-[min(56vw,740px)] max-[860px]:w-[88vw] max-[860px]:max-w-[420px]">
              <Image
                src="/sweet_tray.png"
                alt="Sri Amman Bakery Royal Sweet Tray Platter"
                fill
                priority
                sizes="(max-width: 860px) 90vw, 55vw"
                className="h-full w-full object-contain filter drop-shadow-[0_25px_45px_rgba(7,27,22,0.85)] transition-transform duration-700 ease-[cubic-bezier(.22,.7,.2,1)] group-hover:scale-102"
              />

              {/* Floating Sweet Highlights on Tray (Desktop) */}
              <div className="absolute top-[18%] left-[8%] hidden rounded-full border border-[#C99732]/45 bg-[#0A241E]/90 px-3 py-1 text-[.62rem] font-medium tracking-wider text-[#F7F1E5] uppercase backdrop-blur-md shadow-lg lg:block">
                100% Pure Homemade Ghee Mysore Pak
              </div>

              <div className="absolute top-[8%] right-[22%] hidden rounded-full border border-[#C99732]/45 bg-[#0A241E]/90 px-3 py-1 text-[.62rem] font-medium tracking-wider text-[#F7F1E5] uppercase backdrop-blur-md shadow-lg lg:block">
                Golden Handcrafted Laddu
              </div>

              <div className="absolute bottom-[20%] right-[10%] hidden rounded-full border border-[#C99732]/45 bg-[#0A241E]/90 px-3 py-1 text-[.62rem] font-medium tracking-wider text-[#F7F1E5] uppercase backdrop-blur-md shadow-lg lg:block">
                Boost & Horlicks Burfi
              </div>

              <div className="absolute bottom-[16%] left-[16%] hidden rounded-full border border-[#C99732]/45 bg-[#0A241E]/90 px-3 py-1 text-[.62rem] font-medium tracking-wider text-[#F7F1E5] uppercase backdrop-blur-md shadow-lg lg:block">
                Crisp Saffron Jalebi
              </div>
            </div>

            {/* Bottom Platter Label & Explore Trigger */}
            <div className="mt-4 flex flex-wrap items-center justify-center gap-3 text-center max-[860px]:mt-2">
              <span className="text-[.7rem] font-normal tracking-[.24em] text-[#C99732]/90 uppercase">
                Royal Sweet Platter · All 7 Handcrafted Varieties
              </span>

              <a
                href="#sweets"
                className="inline-flex cursor-pointer items-center gap-2 rounded-full border border-[#C99732]/45 bg-[#0A241E]/80 px-4 py-1.5 text-[.66rem] font-medium tracking-[.2em] text-[#C99732] uppercase transition-all duration-300 hover:bg-[#C99732] hover:text-[#0A241E] hover:shadow-[0_6px_18px_-4px_rgba(201,151,50,0.4)]"
              >
                <span>Explore All 12 Sweets</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
