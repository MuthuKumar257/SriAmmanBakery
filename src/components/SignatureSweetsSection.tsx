"use client";

import React, { useRef } from "react";
import { ArrowRight, Sparkles } from "lucide-react";
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
  subtitle?: string;
  edition: string;
  category: string;
  headline: string;
  description: string;
  tags: string[];
  metrics: { label: string; value: string }[];
  color: string;
  ink: string;
  accent: string;
  image: string;
}

export const signatureSweets: SignatureSweet[] = [
  {
    id: "laddu",
    name: "Laddu",
    edition: "Traditional Classic · Gram Flour Sweet",
    category: "Gram Flour Sweet",
    headline:
      "Golden, round traditional Indian sweet crafted with slow-roasted gram flour, 100% pure homemade ghee, green cardamom, melon seeds, and slivered pistachios.",
    description:
      "Melt-in-the-mouth texture with an aromatic cardamom warmth, subtle nuttiness from slow-roasted gram flour, and a gentle crunch from toasted melon seeds.",
    tags: [
      "Gram Flour",
      "100% Pure Homemade Ghee",
      "Sugar",
      "Melon Seeds",
      "Pistachios",
      "Green Cardamom",
    ],
    metrics: [
      { label: "Ghee Purity", value: "100%" },
      { label: "Shelf Life", value: "15 Days" },
    ],
    color: "#FBF5E8",
    ink: "#123D32",
    accent: "#C99732",
    image: "/sweets/laddu.jpg",
  },
  {
    id: "mysore-pak",
    name: "Mysore Pak",
    edition: "Heritage Specialty · 100% Pure Homemade Ghee",
    category: "Heritage Specialty",
    headline:
      "Rich, golden, traditional gram-flour sweet with a porous, honeycomb crumb that melts luxuriously on the tongue.",
    description:
      "Silky, delicate honeycomb crumb with an unmistakable caramelized ghee aroma and an instant dissolve on the palate.",
    tags: [
      "Gram Flour",
      "100% Pure Homemade Ghee",
      "Sugar",
      "Green Cardamom",
    ],
    metrics: [
      { label: "Ghee Infusion", value: "Generous" },
      { label: "Crumb Structure", value: "Honeycomb" },
    ],
    color: "#FDF4DC",
    ink: "#651B24",
    accent: "#C99732",
    image: "/sweets/mysore-pak.jpg",
  },
  {
    id: "jalebi",
    name: "Jalebi",
    edition: "Festive Spiral Sweet · Crisp & Syrup-Soaked",
    category: "Festive Spiral Sweet",
    headline:
      "Bright orange, syrup-soaked spiral sweet fried crisp to golden perfection and steeped in warm saffron sugar syrup.",
    description:
      "Crisp and crunchy outer shell that bursts with warm, fragrant saffron syrup at the very first bite.",
    tags: [
      "Wheat Flour",
      "100% Pure Homemade Ghee",
      "Saffron Sugar Syrup",
      "Green Cardamom",
    ],
    metrics: [
      { label: "Crispness", value: "High" },
      { label: "Syrup Base", value: "Saffron" },
    ],
    color: "#FFF2E5",
    ink: "#0A241E",
    accent: "#D9681E",
    image: "/sweets/jalebi.jpg",
  },
  {
    id: "badam-burfi",
    name: "Badam Burfi",
    edition: "Diamond Nut Burfi · Royal Almond Delicacy",
    category: "Diamond Nut Burfi",
    headline:
      "Almond-based sweet cut into neat diamond pieces, infused with fragrant cardamom and crowned with pure edible silver foil and slivered almonds.",
    description:
      "Finely ground California almonds cooked with pure homemade ghee and milk, offering an ultra-smooth, delicate nutty texture.",
    tags: [
      "Almonds",
      "Sugar",
      "100% Pure Homemade Ghee",
      "Cardamom",
      "Edible Silver Foil",
    ],
    metrics: [
      { label: "Nut Content", value: "Pure Almond" },
      { label: "Cut Style", value: "Diamond" },
    ],
    color: "#FAF7F0",
    ink: "#651B24",
    accent: "#C99732",
    image: "/sweets/badam-burfi.jpg",
  },
  {
    id: "boost-burfi",
    name: "Boost Burfi",
    edition: "Malted Fudge Specialty · Signature Malt Fudge",
    category: "Malted Fudge Specialty",
    headline:
      "Chocolate-brown malt burfi with an appetizing, rich fudge texture, deep malt aroma, and crunchy embedded cashews.",
    description:
      "Nostalgic malted chocolate-flavored milk fudge slow-cooked in pure homemade ghee with whole toasted cashew bits.",
    tags: [
      "Boost Malt",
      "Milk Solids",
      "100% Pure Homemade Ghee",
      "Cashews",
      "Sugar",
    ],
    metrics: [
      { label: "Malt Profile", value: "Chocolate" },
      { label: "Texture", value: "Rich Fudge" },
    ],
    color: "#1E1614",
    ink: "#F7E6CA",
    accent: "#E0B04E",
    image: "/sweets/boost-burfi.jpg",
  },
  {
    id: "horlicks-burfi",
    name: "Horlicks Burfi",
    edition: "Golden Malted Specialty · Creamy Malted Square",
    category: "Golden Malted Specialty",
    headline:
      "Malt-flavored burfi presented in clean, attractive square pieces with a delicate milky aroma and toasted slivered nuts.",
    description:
      "Creamy, golden malt-infused milk confection slow-stirred with 100% pure homemade ghee and adorned with crunchy cashews.",
    tags: [
      "Horlicks Malt",
      "Milk Solids",
      "100% Pure Homemade Ghee",
      "Cashews",
      "Sugar",
    ],
    metrics: [
      { label: "Malt Profile", value: "Golden" },
      { label: "Melt Profile", value: "Creamy" },
    ],
    color: "#F6EEDC",
    ink: "#2D1D14",
    accent: "#C99732",
    image: "/sweets/horlicks-burfi.jpg",
  },
  {
    id: "badusha",
    name: "Badusha",
    edition: "Layered Festive Pastry · Traditional Layered Pastry",
    category: "Layered Festive Pastry",
    headline:
      "A traditional Indian sweet with a golden exterior, delicate layers, and a rich, sweet finish.",
    description:
      "Flaky, layered glazed pastry with a tender crumb fried gently in pure homemade ghee to golden perfection.",
    tags: [
      "Refined Wheat Flour",
      "100% Pure Homemade Ghee",
      "Sugar",
      "Cardamom",
    ],
    metrics: [
      { label: "Crumb", value: "Tender Layered" },
      { label: "Fry Style", value: "Slow Ghee" },
    ],
    color: "#FAF3E6",
    ink: "#123D32",
    accent: "#651B24",
    image: "/sweets/badusha.jpg",
  },
  {
    id: "carrot-burfi",
    name: "Carrot Burfi",
    edition: "Fresh Carrot Confectionery · Fresh Garden Delicacy",
    category: "Fresh Carrot Confectionery",
    headline:
      "Vibrant orange traditional sweet prepared with freshly grated garden carrots, slow-condensed milk, 100% pure homemade ghee, cardamom, and toasted cashews.",
    description:
      "Slow-simmered farm carrots reduced in rich whole milk and pure homemade ghee for an authentically succulent texture.",
    tags: [
      "Fresh Carrots",
      "Milk Solids",
      "100% Pure Homemade Ghee",
      "Cardamom",
      "Cashews",
    ],
    metrics: [
      { label: "Garden Fresh", value: "100%" },
      { label: "Simmer Time", value: "4 Hours" },
    ],
    color: "#FFF0E6",
    ink: "#123D32",
    accent: "#E65C24",
    image: "/sweets/carrot-burfi.jpg",
  },
  {
    id: "pista-burfi",
    name: "Pista Burfi",
    edition: "Diamond Nut Confectionery · Royal Pistachio Delicacy",
    category: "Diamond Nut Confectionery",
    headline:
      "Luxurious pastel-green diamond burfi crafted from premium ground pistachios, condensed whole milk, pure homemade ghee, and cardamom.",
    description:
      "Finely ground rich emerald pistachios combined with slow-condensed milk, cut into delicate royal diamond shapes.",
    tags: [
      "Pistachios",
      "Milk Solids",
      "100% Pure Homemade Ghee",
      "Cardamom",
      "Sugar",
    ],
    metrics: [
      { label: "Pistachio Grade", value: "Premium" },
      { label: "Texture", value: "Velvety" },
    ],
    color: "#EDF5EA",
    ink: "#163828",
    accent: "#4A7C59",
    image: "/sweets/pista-burfi.jpg",
  },
  {
    id: "rose-burfi",
    name: "Rose Burfi",
    edition: "Infused Milk Specialty · Floral Rose Fudge",
    category: "Infused Milk Specialty",
    headline:
      "Fragrant pink confectionery infused with damask rose petals, rose water, slow-condensed milk solids, and 100% pure homemade ghee.",
    description:
      "Delicate and aromatic milk fudge delicately scented with natural rose water and studded with slivered nuts.",
    tags: [
      "Milk Solids",
      "100% Pure Homemade Ghee",
      "Rose Water",
      "Cardamom",
      "Sugar",
    ],
    metrics: [
      { label: "Essence", value: "Damask Rose" },
      { label: "Finish", value: "Aromatic" },
    ],
    color: "#FAF0F2",
    ink: "#581827",
    accent: "#C25975",
    image: "/sweets/rose-burfi.jpg",
  },
  {
    id: "gulab-jamun",
    name: "Gulab Jamun",
    edition: "Heritage Festive Confectionery · Classic Syrup-Soaked",
    category: "Heritage Festive Confectionery",
    headline:
      "Deep golden spheres crafted from slow-reduced milk solids, gently fried in 100% pure homemade ghee and steeped in fragrant cardamom sugar syrup.",
    description:
      "Ultra-soft melt-in-mouth dumplings soaked in warm rose and cardamom-scented sugar syrup for a heavenly dessert.",
    tags: [
      "Milk Solids",
      "Wheat Flour",
      "100% Pure Homemade Ghee",
      "Cardamom",
      "Rose Water",
    ],
    metrics: [
      { label: "Fried In", value: "100% Pure Ghee" },
      { label: "Soak", value: "Cardamom Syrup" },
    ],
    color: "#FFF5EA",
    ink: "#2B1610",
    accent: "#C99732",
    image: "/sweets/gulab-jamun.jpg",
  },
  {
    id: "milk-laddu",
    name: "Milk Laddu",
    subtitle: "Also called Tirupathi Laddu",
    edition: "Heritage Milk Laddu · Celebration Specialty",
    category: "Heritage Milk Laddu",
    headline:
      "A traditional, round Indian sweet known for its rich taste, soft texture, and delightful sweetness. A lovely choice for celebrations, family gatherings, and special occasions.",
    description:
      "Rich, soft, and crumbly with slow-simmered milk sweetness, generous pure homemade ghee, whole cashews, plump raisins, and green cardamom.",
    tags: [
      "Milk Solids",
      "Gram Flour",
      "100% Pure Homemade Ghee",
      "Cashews",
      "Raisins",
      "Green Cardamom",
    ],
    metrics: [
      { label: "Occasion", value: "Celebrations" },
      { label: "Texture", value: "Soft & Crumbly" },
    ],
    color: "#FBF7EF",
    ink: "#123D32",
    accent: "#651B24",
    image: "/sweets/milk-laddu.jpg",
  },
];

interface SignatureSweetsSectionProps {
  onSelectSweet?: (sweetName: string) => void;
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
                { yPercent: 12, rotate: -2 },
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
      id="sweets"
      data-tone="light"
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
            <span className="mb-4 inline-flex items-center gap-2 rounded-full border border-[#C99732]/40 bg-[#C99732]/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.25em] text-[#C99732]">
              <Sparkles className="size-3.5" /> Sri Amman Bakery · Established 2022
            </span>
            <h2 className="text-[clamp(3.5rem,13vw,13rem)] font-bold tracking-tight leading-[0.85] uppercase">
              Signature<br />Sweets
              <span className="veil-dot ml-2 inline-block size-[0.16em] rounded-full align-baseline bg-[#C99732] shadow-[0_0_24px_rgba(201,151,50,0.6)]" />
            </h2>
            <p className="mt-8 max-w-md text-lg text-white/70">
              Handcrafted daily with 100% pure homemade ghee. Twelve artisanal traditional specialties prepared fresh daily.
            </p>
          </div>
        </div>

        {/* 12 Traditional Sweets Chapters (Sticky Stacking Deck) */}
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
                  <div className="flex items-center gap-3">
                    <span
                      className="text-xs font-bold uppercase tracking-[0.2em]"
                      style={{ color: sweet.accent }}
                    >
                      {sweet.edition}
                    </span>
                    <span className="text-xs font-medium opacity-50">
                      · {String(idx + 1).padStart(2, "0")} / 12
                    </span>
                  </div>

                  <h3 className="sweet-title mt-3 font-serif text-[clamp(2.75rem,5.5vw,6.5rem)] font-extrabold leading-[0.9] tracking-tight">
                    {sweet.name}
                  </h3>

                  {sweet.subtitle && (
                    <p
                      className="mt-1 text-sm font-semibold italic"
                      style={{ color: sweet.accent }}
                    >
                      {sweet.subtitle}
                    </p>
                  )}

                  <p className="mt-5 text-[clamp(1.1rem,1.7vw,1.65rem)] font-medium leading-snug">
                    {sweet.headline}
                  </p>

                  <p className="mt-4 text-base leading-relaxed opacity-85">
                    {sweet.description}
                  </p>

                  {/* Ingredients & Flavor Tags */}
                  <ul className="mt-6 flex flex-wrap gap-2">
                    {sweet.tags.map((tag) => (
                      <li
                        key={tag}
                        className="rounded-full border border-current/20 bg-current/5 px-3.5 py-1 text-xs font-semibold tracking-wide"
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
                      onClick={() => onSelectSweet?.(sweet.name)}
                      className="group inline-flex h-12 items-center gap-2 rounded-full px-7 text-sm font-semibold shadow-lg transition-all duration-200 hover:scale-105 active:scale-95 cursor-pointer"
                      style={{ backgroundColor: sweet.ink, color: sweet.color }}
                    >
                      <span>View Sweet Profile</span>
                      <ArrowRight className="size-4 transition-transform group-hover:translate-x-1" />
                    </button>
                    <button
                      onClick={() => onSelectSweet?.(sweet.name)}
                      className="inline-flex h-12 items-center gap-2 rounded-full border border-current px-6 text-sm font-semibold transition-all duration-200 hover:bg-current/10 active:scale-95 cursor-pointer"
                    >
                      <span>Tasting Notes</span>
                      <Sparkles className="size-4" />
                    </button>
                  </div>
                </div>

                {/* Right Hero Sweet Image (55% width) with 3D Parallax Tilt */}
                <figure className="relative mt-8 flex flex-1 items-center justify-center md:mt-0">
                  <div className="relative group cursor-pointer" onClick={() => onSelectSweet?.(sweet.name)}>
                    <img
                      src={sweet.image}
                      alt={sweet.name}
                      className="sweet-hero-img max-h-[62svh] w-auto max-w-full rounded-2xl object-cover drop-shadow-[0_40px_80px_rgba(0,0,0,0.55)] transition-transform duration-500 will-change-transform group-hover:scale-105"
                    />
                    <div className="pointer-events-none absolute inset-0 rounded-2xl ring-1 ring-black/10" />
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
