"use client";

import React, { useEffect, useRef, useState } from "react";
import Image from "next/image";
import { siteConfig } from "@/config/site";
import { clamp, lerp, prefersReducedMotion } from "@/lib/utils";

interface PackSectionProps {
  onOpenOrder: (productName?: string) => void;
}

const GARNISH_IMAGES = [1, 2, 3, 4, 5, 6, 7].map((i) => `/garnishes/${i}.png`);
const ASPECT = 1.0;
const randRange = (spread: number) => (Math.random() - 0.5) * 2 * spread;

interface GarnishEntity {
  el: HTMLImageElement;
  shadow: HTMLDivElement;
  size: number;
  depth: number;
  restX: number;
  ground: number;
  restRot: number;
  delay: number;
  bounce: number;
  x: number;
  y: number;
  vx: number;
  vy: number;
  rot: number;
  vr: number;
  wait: number;
  landed: boolean;
  still: boolean;
}

// Falling Dry Fruits / Garnishes Physics Simulation
const FallingGarnishes: React.FC<{
  play: boolean;
  avoidRef: React.RefObject<HTMLDivElement | null>;
}> = ({ play, avoidRef }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const controllerRef = useRef<{ start: () => void; clear: () => void } | null>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    let items: GarnishEntity[] = [];
    let clientH = 1;
    let scaleFactor = 1;
    let animId = 0;
    let state: "cleared" | "falling" | "resting" = "cleared";

    const updateDomTransform = (item: GarnishEntity) => {
      const h = item.size * ASPECT;
      item.el.style.transform = `translate3d(${item.x - item.size / 2}px, ${
        item.y - h / 2
      }px, 0) rotate(${item.rot}deg)`;

      const distNorm = 1 - clamp((item.ground - item.y) / (260 * scaleFactor));
      const shadowW = item.size * lerp(1.5, 0.92, distNorm);

      item.shadow.style.transform = `translate3d(${item.x - shadowW / 2}px, ${
        item.ground + h * 0.3
      }px, 0)`;
      item.shadow.style.width = `${shadowW}px`;
      item.shadow.style.opacity = String(
        item.y < -h ? 0 : lerp(0.15, 1, distNorm * distNorm)
      );
    };

    const restAll = () => {
      cancelAnimationFrame(animId);
      state = "resting";
      for (const item of items) {
        Object.assign(item, {
          x: item.restX,
          y: item.ground,
          rot: item.restRot,
          still: true,
        });
        updateDomTransform(item);
      }
    };

    const clearAll = () => {
      cancelAnimationFrame(animId);
      state = "cleared";
      for (const item of items) {
        item.y = -item.size * 2;
        updateDomTransform(item);
      }
    };

    const initEntities = () => {
      container.replaceChildren();
      const clientW = container.clientWidth;
      clientH = container.clientHeight;
      scaleFactor = clamp(clientW / 1440, 0.62, 1.15);

      const count = clamp(Math.round(clientW / 23), 22, 76);
      const contRect = container.getBoundingClientRect();
      const avoidRect = avoidRef.current?.getBoundingClientRect();

      const hasAvoid = avoidRect && avoidRect.width < clientW * 0.5;
      const avoidLeft = hasAvoid
        ? avoidRect.left - contRect.left + avoidRect.width * 0.1
        : clientW / 2;
      const avoidRight = hasAvoid
        ? avoidRect.right - contRect.left - avoidRect.width * 0.05
        : clientW / 2;

      items = Array.from({ length: count }, (_, idx) => {
        const depth = Math.random();
        const size =
          lerp(44, 90, depth) *
          scaleFactor *
          (0.88 + Math.random() * 0.24);

        let posX = ((idx + 0.15 + Math.random() * 0.7) / count) * clientW;
        if (hasAvoid && posX > avoidLeft - size * 0.4 && posX < avoidRight + size * 0.4) {
          posX =
            posX < (avoidLeft + avoidRight) / 2
              ? avoidLeft - size * 0.4 - Math.random() * clientW * 0.14
              : avoidRight + size * 0.4 + Math.random() * clientW * 0.14;
        }

        const imgEl = new window.Image();
        imgEl.src = GARNISH_IMAGES[idx % GARNISH_IMAGES.length];
        imgEl.alt = "";
        imgEl.draggable = false;
        imgEl.style.cssText = `position:absolute;left:0;top:0;width:${size}px;height:auto;max-width:none;will-change:transform;z-index:${
          10 + Math.round(depth * 100)
        };`;

        const shadowEl = document.createElement("div");
        shadowEl.style.cssText = `position:absolute;left:0;top:0;height:${
          size * 0.22
        }px;border-radius:50%;background:radial-gradient(closest-side,rgba(58,28,8,0.38),rgba(58,28,8,0));will-change:transform,opacity;z-index:${
          9 + Math.round(depth * 100)
        };`;

        container.append(shadowEl, imgEl);

        return {
          el: imgEl,
          shadow: shadowEl,
          size,
          depth,
          restX: posX,
          ground: clientH - lerp(96, 12, depth) * scaleFactor - size * ASPECT * 0.5,
          restRot: randRange(70),
          delay: Math.pow(Math.random(), 1.4) * 1.5,
          bounce: 0.26 + Math.random() * 0.14,
          x: posX,
          y: -200,
          vx: 0,
          vy: 0,
          rot: 0,
          vr: 0,
          wait: 0,
          landed: false,
          still: false,
        };
      });

      if (state === "cleared") clearAll();
      else restAll();
    };

    controllerRef.current = {
      start: () => {
        if (state !== "cleared") return;
        if (prefersReducedMotion()) return restAll();

        state = "falling";
        for (const item of items) {
          Object.assign(item, {
            x: item.restX + randRange(24 * scaleFactor),
            y: -item.size - Math.random() * clientH * 0.25,
            vx: 0,
            vy: 120 * scaleFactor,
            rot: randRange(180),
            vr: randRange(420),
            wait: item.delay,
            landed: false,
            still: false,
          });
          updateDomTransform(item);
        }

        const gravity = 2500 * clamp(clientH / 900, 0.7, 1.4);
        let lastTimestamp = performance.now();

        const stepPhysics = (now: number) => {
          const delta = Math.min((now - lastTimestamp) / 1000, 0.034);
          lastTimestamp = now;
          let anyMoving = false;

          for (const item of items) {
            if (!item.still) {
              anyMoving = true;
              if (item.wait > 0) {
                item.wait -= delta;
                continue;
              }

              item.vy += gravity * delta;
              item.y += item.vy * delta;
              item.x += item.vx * delta;
              item.rot += item.vr * delta;

              if (item.y >= item.ground) {
                item.y = item.ground;
                if (item.vy > 300 * scaleFactor) {
                  item.vy = -item.vy * item.bounce;
                  item.vx = randRange(item.landed ? 40 : 110) * scaleFactor;
                  item.vr = randRange(item.landed ? 160 : 380);
                  item.landed = true;
                } else {
                  item.vy = 0;
                  const damping = Math.exp(-9 * delta);
                  item.vx *= damping;
                  item.vr *= damping;
                  if (Math.abs(item.vr) < 6 && Math.abs(item.vx) < 3) {
                    item.still = true;
                  }
                }
              }
              updateDomTransform(item);
            }
          }

          if (anyMoving) {
            animId = requestAnimationFrame(stepPhysics);
          } else {
            state = "resting";
          }
        };

        animId = requestAnimationFrame(stepPhysics);
      },
      clear: clearAll,
    };

    initEntities();
    window.addEventListener("resize", initEntities);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", initEntities);
      controllerRef.current = null;
      container.replaceChildren();
    };
  }, [avoidRef]);

  useEffect(() => {
    if (play) {
      controllerRef.current?.start();
    } else {
      controllerRef.current?.clear();
    }
  }, [play]);

  return (
    <div
      ref={containerRef}
      aria-hidden="true"
      className="pointer-events-none absolute inset-0 overflow-hidden"
    />
  );
};

export const PackSection: React.FC<PackSectionProps> = ({ onOpenOrder }) => {
  const sectionRef = useRef<HTMLElement>(null);
  const boxRef = useRef<HTMLDivElement>(null);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);

  useEffect(() => {
    const sec = sectionRef.current;
    if (!sec) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        const topPast = entry.boundingClientRect.top < 0;
        if (entry.intersectionRatio >= (topPast ? 0.12 : 0.45)) {
          setIsPlaying(true);
        } else if (!entry.isIntersecting) {
          setIsPlaying(false);
        }
      },
      { threshold: [0, 0.12, 0.45] }
    );

    observer.observe(sec);
    return () => observer.disconnect();
  }, []);

  const featureClass =
    "flex items-center gap-4 text-[.72rem] font-normal tracking-[.24em] uppercase text-[#123D32] before:h-px before:w-9 before:shrink-0 before:bg-[#C99732]";

  return (
    <section
      id="pack"
      ref={sectionRef}
      data-tone="light"
      data-play={isPlaying}
      className="pack-bg relative isolate h-svh min-h-[640px] overflow-hidden text-[#123D32]"
    >
      {/* Top Heading & CTA */}
      <div className="relative z-[5] px-(--pad) pt-[clamp(92px,13vh,132px)] text-center">
        <h2 className="font-serif text-[clamp(2.3rem,4.5vw,4.6rem)] leading-[1.02] font-medium tracking-[-.015em] text-[#123D32]">
          {siteConfig.pack.heading}{" "}
          <em className="font-normal text-[#651B24]">{siteConfig.pack.accent}</em>
        </h2>

        {/* Subtitle on Mobile */}
        <p className="mt-3 hidden text-[.72rem] font-normal tracking-[.24em] text-[#123D32]/75 uppercase max-[860px]:block">
          {siteConfig.pack.mobileSubtitle}
        </p>

        {/* Action Navigation */}
        <div className="mt-[clamp(18px,3vh,30px)] flex items-center justify-center gap-4">
          <a
            href="#sweets"
            className="cursor-pointer rounded-full bg-[#123D32] border border-[#C99732]/45 px-10 py-4 indent-[.28em] text-[.72rem] font-medium tracking-[.28em] text-[#F7F1E5] uppercase shadow-[0_10px_24px_-10px_rgba(18,61,50,.65)] transition-all duration-300 hover:-translate-y-0.5 hover:bg-[#651B24] hover:border-[#C99732] hover:shadow-[0_16px_28px_-12px_rgba(101,27,36,.6)] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#C99732]"
          >
            Explore All 12 Sweets
          </a>

          <button
            type="button"
            onClick={() => onOpenOrder("Laddu")}
            className="cursor-pointer rounded-full border border-[#123D32]/35 bg-transparent px-6 py-4 text-[.72rem] font-medium tracking-[.24em] text-[#123D32] uppercase transition-all duration-300 hover:border-[#651B24] hover:bg-[#651B24]/10 hover:text-[#651B24] max-[860px]:hidden"
          >
            View Sweet Profiles
          </button>
        </div>
      </div>

      {/* Floating Left Features */}
      <ul className="absolute top-[58%] right-[calc(50%+min(21vh,27vw)+clamp(28px,4vw,72px))] z-[5] grid -translate-y-1/2 justify-items-end gap-[clamp(14px,2.6vh,26px)] max-[860px]:hidden">
        {siteConfig.pack.product.highlightsLeft.map((feat) => (
          <li key={feat} className={`${featureClass} flex-row-reverse`}>
            {feat}
          </li>
        ))}
      </ul>

      {/* Floating Right Features */}
      <ul className="absolute top-[58%] left-[calc(50%+min(21vh,27vw)+clamp(28px,4vw,72px))] z-[5] grid -translate-y-1/2 gap-[clamp(14px,2.6vh,26px)] max-[860px]:hidden">
        {siteConfig.pack.product.highlightsRight.map((feat) => (
          <li key={feat} className={featureClass}>
            {feat}
          </li>
        ))}
      </ul>

      {/* Falling Dry Fruits & Garnish Animation */}
      <FallingGarnishes play={isPlaying} avoidRef={boxRef} />

      {/* Central Luxury Sweet Box Display */}
      <div
        ref={boxRef}
        className="absolute bottom-[5.5%] left-1/2 z-[44] h-[56vh] -translate-x-1/2 max-[860px]:bottom-[12%] max-[860px]:z-[5] max-[860px]:h-[min(50vh,93vw)]"
      >
        <div aria-hidden="true" className="pack-glow absolute inset-[-18%] -z-10" />
        <div
          aria-hidden="true"
          className="pack-floor absolute inset-x-[8%] bottom-[-1.5%] -z-10 h-[9%]"
        />
        <Image
          src="/package.png"
          alt={`${siteConfig.brandName} - ${siteConfig.pack.product.name}`}
          width={926}
          height={1024}
          priority
          className="pack-shot block h-full w-auto max-w-none object-contain"
        />
      </div>
    </section>
  );
};
