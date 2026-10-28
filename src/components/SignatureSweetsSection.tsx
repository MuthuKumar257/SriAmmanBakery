"use client";

import React, { useRef } from "react";
import { ArrowRight, Plus, Sparkles } from "lucide-react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { SplitText } from "gsap/SplitText";
import { useGSAP } from "@gsap/react";

if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger, SplitText);
}

export interface SignatureSweet {
  id: string;
  name: string;
  edition: string;
  headline: string;
  description: string;
  tags: string[];
  metrics: { label: string; value: string }[];
  color: string;
  ink: string;
  image: string;
}

export const signatureSweets: SignatureSweet[] = [
  {
    id: "baklava",
    name: "Pistachio Baklava",
    edition: "Grand Reserve · 48 Layers",
    headline: "Hand-stretched filo ribbons infused with Iranian saffron syrup.",
    description:
      "Slow-baked with crushed Antep wild pistachios and finished with a crystalline amber honey glaze.",
    tags: ["Wild Pistachio", "Organic Saffron", "Wildflower Honey"],
    metrics: [
      { label: "Flaky Layers", value: "48" },
      { label: "Sweetness Index", value: "3 / 5" },
    ],
    color: "#E6EBD9",
    ink: "#1A3323",
    image: "/assets/sweets/baklava.png",
  },
  {
    id: "truffle",
    name: "Midnight Truffle",
    edition: "Single Origin · 74% Cacao",
    headline:
      "Silky ganache enrobed in obsidian cocoa and 24K edible gold leaf.",
    description:
      "Crafted from Venezuelan single-estate beans paired with bourbon vanilla and smoked sea salt crystals.",
    tags: ["74% Single-Estate", "Bourbon Vanilla", "Smoked Salt"],
    metrics: [
      { label: "Cacao Purity", value: "74%" },
      { label: "Sweetness Index", value: "2 / 5" },
    ],
    color: "#1E1614",
    ink: "#F3E5AB",
    image: "/assets/sweets/truffle.png",
  },
  {
    id: "rose-delight",
    name: "Rose & Cardamom",
    edition: "Botanical Atelier · Velvet Cube",
    headline:
      "Subtle Damascus rose water laced with stone-ground green cardamom.",
    description:
      "Dusted with toasted Turkish hazelnuts and natural ruby beetroot powder for a silky melt-in-mouth finish.",
    tags: ["Damascus Rose", "Mysore Cardamom", "Toasted Hazelnut"],
    metrics: [
      { label: "Melt Profile", value: "Slow" },
      { label: "Sweetness Index", value: "3.5 / 5" },
    ],
    color: "#F5E6E8",
    ink: "#3E1821",
    image: "/assets/sweets/rose-delight.png",
  },
  {
    id: "honey-peda",
    name: "Honey Caramel Peda",
    edition: "Heritage Gold · Milk Reduction",
    headline:
      "Slow-caramelized farm milk fudge infused with raw wildflower forest honey.",
    description:
      "Simmered in shallow pans until deeply golden, kissed with nutmeg and stamped with an heirloom crest.",
    tags: ["Caramelized Khoya", "Wild Honey", "Mace & Nutmeg"],
    metrics: [
      { label: "Reduction Time", value: "6 Hours" },
      { label: "Sweetness Index", value: "3 / 5" },
    ],
    color: "#F4E8D1",
    ink: "#2A1810",
    image: "/assets/sweets/honey-peda.png",
  },
];

interface SignatureSweetsSectionProps {
  onSelectSweet?: (sweet: SignatureSweet) => void;
}

export function SignatureSweetsSection({
  onSelectSweet,
}: SignatureSweetsSectionProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      const section = containerRef.current;
      if (!section) return;

      const mm = gsap.matchMedia();
      const sheets = gsap.utils.toArray<HTMLElement>(".sweet-sheet");
      const markers = gsap.utils.toArray<HTMLElement>(".sheet-marker");
      const veil = section.querySelector<HTMLElement>(".sweets-veil");
      const dot = section.querySelector<HTMLElement>(".veil-dot");

      mm.add(
        "(min-width: 768px) and (min-height: 640px) and (prefers-reduced-motion: no-preference)",
        () => {
          // 1. Iris Aperture Reveal
          if (veil && dot) {
            const updateIrisCoords = () => {
              const rect = dot.getBoundingClientRect();
              const vRect = veil.getBoundingClientRect();
              const cx = rect.left - vRect.left + rect.width / 2;
              const cy = rect.top - vRect.top + rect.height / 2;
              const maxRadius =
                Math.hypot(
                  Math.max(cx, vRect.width - cx),
                  Math.max(cy, vRect.height - cy)
                ) + 4;
              veil.style.setProperty("--iris-x", `${cx}px`);
              veil.style.setProperty("--iris-y", `${cy}px`);
              return maxRadius;
            };

            const maxRadius = updateIrisCoords();

            gsap
              .timeline({
                scrollTrigger: {
                  trigger: ".sweets-stack",
                  start: "top top",
                  end: () => `+=${window.innerHeight * 1.1}`,
                  scrub: 0.6,
                  invalidateOnRefresh: true,
                  onRefreshInit: updateIrisCoords,
                },
              })
              .fromTo(
                veil,
                { "--iris-r": "0px" },
                {
                  "--iris-r": `${maxRadius}px`,
                  ease: "power2.in",
                  duration: 1,
                }
              )
              .to(".veil-content", { scale: 1.16, ease: "power1.in", duration: 1 }, 0)
              .set(veil, { autoAlpha: 0 }, 1);
          }

          // 2. Stacking Cards Depth, Corner Rounding & Scale Physics
          sheets.slice(0, -1).forEach((sheet, idx) => {
            gsap
              .timeline({
                scrollTrigger: {
                  trigger: markers[idx + 1],
                  start: "top bottom",
                  end: "top top",
                  scrub: true,
                },
              })
              .to(sheet, { scale: 0.9, borderRadius: "28px", ease: "none" }, 0)
              .to(
                sheet.querySelector(".sheet-shade"),
                { opacity: 0.45, ease: "none" },
                0
              );
          });

          // 3. Parallax Sweet Art + Character Split
          sheets.forEach((sheet, idx) => {
            const art = sheet.querySelector<HTMLElement>(".sweet-hero-img");
            if (art && idx > 0) {
              gsap.fromTo(
                art,
                { yPercent: 14, rotate: -3 },
                {
                  yPercent: 0,
                  rotate: 0,
                  ease: "none",
                  scrollTrigger: {
                    trigger: markers[idx],
                    start: "top bottom",
                    end: "top top",
                    scrub: true,
                  },
                }
              );
            }

            const titleEl = sheet.querySelector<HTMLElement>(".sweet-title");
            if (titleEl && idx > 0) {
              try {
                const split = new SplitText(titleEl, {
                  type: "words,chars",
                  charsClass: "char-mask",
                  autoSplit: true,
                });

                gsap.from(split.chars, {
                  yPercent: 140,
                  duration: 1,
                  ease: "expo.out",
                  stagger: 0.025,
                  scrollTrigger: {
                    trigger: markers[idx],
                    start: "top 55%",
                    toggleActions: "play none none reverse",
                  },
                });
              } catch (e) {
                console.warn("SplitText initialization error:", e);
              }
            }
          });
        }
      );

      // Reduced motion / mobile fallback
      mm.add(
        "(max-width: 767px), (max-height: 639px), (prefers-reduced-motion: reduce)",
        () => {
          if (veil) {
            gsap.set(veil, { display: "none" });
          }
        }
      );
    },
    { scope: containerRef }
  );

  return (
    <section
      id="signature-collection"
      ref={containerRef}
      className="relative bg-[#0c0d0c] text-white"
    >
      <div className="sweets-stack relative flow-root">
        {/* Iris Intro Veil */}
        <div
          className="sweets-veil pointer-events-none sticky top-0 z-20 h-[100svh] -mb-[100svh] overflow-clip bg-[#0c0d0c]"
          style={{
            maskImage:
              "radial-gradient(circle at var(--iris-x, 50%) var(--iris-y, 50%), transparent var(--iris-r, 0px), #000 calc(var(--iris-r, 0px) + 1px))",
            WebkitMaskImage:
              "radial-gradient(circle at var(--iris-x, 50%) var(--iris-y, 50%), transparent var(--iris-r, 0px), #000 calc(var(--iris-r, 0px) + 1px))",
          }}
        >
          <div className="veil-content flex min-h-[100svh] flex-col items-center justify-center px-6 text-center">
            <span className="mb-4 inline-flex items-center gap-2 rounded-full border border-white/20 bg-white/5 px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.25em] text-[#C99732]">
              <Sparkles className="size-3.5" /> Our Signature Sweets Collection
            </span>
            <h2 className="text-[clamp(3.5rem,13vw,13rem)] font-bold tracking-tight leading-[0.85] uppercase">
              Signature<br />Sweets
              <span className="veil-dot ml-2 inline-block size-[0.16em] rounded-full align-baseline bg-[#EAD9B8] shadow-[0_0_24px_rgba(234,217,184,0.6)]" />
            </h2>
            <p className="mt-8 max-w-md text-lg text-white/70">
              An artisanal tasting collection, slow-crafted in limited daily batches.
            </p>
          </div>
        </div>

        {/* Sweets Chapters (Sticky Stacking Deck) */}
        {signatureSweets.map((sweet, idx) => (
          <div key={sweet.id} className="contents">
            <span className="sheet-marker block h-0" aria-hidden="true" />
            <article
              data-index={idx}
              className={`sweet-sheet relative overflow-hidden transition-shadow md:sticky md:top-0 ${
                idx === 0
                  ? "md:mb-[142svh]"
                  : idx === signatureSweets.length - 1
                  ? "md:mb-0 md:rounded-t-[28px]"
                  : "md:mb-[42svh] md:rounded-t-[28px]"
              } shadow-2xl`}
              style={{ backgroundColor: sweet.color, color: sweet.ink }}
            >
              <div className="relative flex min-h-[100svh] flex-col justify-between px-6 pb-12 pt-24 md:flex-row md:items-center md:px-16 lg:px-24">
                {/* Left Description Column (45% width) */}
                <div className="relative z-10 flex flex-1 flex-col md:max-w-[46%]">
                  <span className="text-xs font-semibold uppercase tracking-[0.2em] opacity-75">
                    {sweet.edition}
                  </span>

                  <h3 className="sweet-title mt-3 text-[clamp(2.75rem,5.5vw,6.5rem)] font-extrabold leading-[0.9] tracking-tight">
                    {sweet.name}
                  </h3>

                  <p className="mt-5 text-[clamp(1.15rem,1.8vw,1.75rem)] font-medium leading-snug">
                    {sweet.headline}
                  </p>

                  <p className="mt-4 text-base leading-relaxed opacity-85">
                    {sweet.description}
                  </p>

                  {/* Flavor Note Tags */}
                  <ul className="mt-6 flex flex-wrap gap-2">
                    {sweet.tags.map((tag) => (
                      <li
                        key={tag}
                        className="rounded-full border border-current/25 px-3.5 py-1 text-xs font-semibold tracking-wide"
                      >
                        {tag}
                      </li>
                    ))}
                  </ul>

                  {/* Signature Metrics */}
                  <dl className="mt-8 flex gap-10">
                    {sweet.metrics.map((m) => (
                      <div key={m.label}>
                        <dt className="text-xs font-medium uppercase tracking-wider opacity-70">
                          {m.label}
                        </dt>
                        <dd className="mt-1 text-2xl font-bold tabular-nums">
                          {m.value}
                        </dd>
                      </div>
                    ))}
                  </dl>

                  {/* Action CTA Buttons */}
                  <div className="mt-10 flex flex-wrap items-center gap-4">
                    <button
                      onClick={() => onSelectSweet?.(sweet)}
                      className="group inline-flex h-12 items-center gap-2 rounded-full px-7 text-sm font-semibold shadow-lg transition-all duration-200 hover:scale-105 active:scale-95 cursor-pointer"
                      style={{ backgroundColor: sweet.ink, color: sweet.color }}
                    >
                      <span>Add to Tasting Box</span>
                      <Plus className="size-4 transition-transform group-hover:rotate-90" />
                    </button>
                    <button
                      onClick={() => onSelectSweet?.(sweet)}
                      className="inline-flex h-12 items-center gap-2 rounded-full border border-current px-6 text-sm font-semibold transition-all duration-200 hover:bg-current/10 active:scale-95 cursor-pointer"
                    >
                      <span>Tasting Notes</span>
                      <ArrowRight className="size-4 transition-transform group-hover:translate-x-1" />
                    </button>
                  </div>
                </div>

                {/* Right Hero Sweet Image (55% width) with 3D Parallax Tilt */}
                <figure className="relative mt-8 flex flex-1 items-center justify-center md:mt-0">
                  <div className="relative">
                    <img
                      src={sweet.image}
                      alt={sweet.name}
                      className="sweet-hero-img max-h-[65svh] w-auto max-w-full rounded-2xl object-contain drop-shadow-[0_40px_80px_rgba(0,0,0,0.55)] transition-transform duration-500 will-change-transform"
                    />
                  </div>
                </figure>
              </div>

              {/* Inner dark scrim simulating ambient depth shadow when sliding underneath */}
              <div
                className="sheet-shade pointer-events-none absolute inset-0 bg-black opacity-0 transition-opacity"
                aria-hidden="true"
              />
            </article>
          </div>
        ))}
      </div>
    </section>
  );
}
