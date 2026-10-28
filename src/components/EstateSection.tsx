"use client";

import React, { useEffect, useRef, useState } from "react";
import Image from "next/image";
import { siteConfig } from "@/config/site";
import { clamp, easeInOutCubic, lerp, norm, prefersReducedMotion } from "@/lib/utils";

const TOTAL_STIR_FRAMES = 55;
const SEAL_RADIUS = 82;
const SEAL_CIRCUMFERENCE = 2 * Math.PI * SEAL_RADIUS;

export const EstateSection: React.FC = () => {
  const sectionRef = useRef<HTMLElement>(null);
  const clipDivRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const scrimRef = useRef<HTMLDivElement>(null);
  const headerRef = useRef<HTMLDivElement>(null);
  const sealRef = useRef<HTMLDivElement>(null);
  const sealSvgRef = useRef<SVGSVGElement>(null);
  const copyRef = useRef<HTMLDivElement>(null);
  const cardDivRef = useRef<HTMLDivElement>(null);
  const cardImgRef = useRef<HTMLImageElement>(null);

  const [activeChapter, setActiveChapter] = useState<number>(0);
  const chapters = siteConfig.estate.chapters;

  useEffect(() => {
    const sec = sectionRef.current;
    const clipDiv = clipDivRef.current;
    const canvas = canvasRef.current;
    const scrim = scrimRef.current;
    const header = headerRef.current;
    const seal = sealRef.current;
    const sealSvg = sealSvgRef.current;
    const copy = copyRef.current;
    const cardDiv = cardDivRef.current;
    const cardImg = cardImgRef.current;

    if (
      !sec ||
      !clipDiv ||
      !canvas ||
      !scrim ||
      !header ||
      !seal ||
      !sealSvg ||
      !copy ||
      !cardDiv ||
      !cardImg
    )
      return;

    const ctx = canvas.getContext("2d", { alpha: false });
    if (!ctx) return;

    const reduced = prefersReducedMotion();

    // -------------------------------------------------------------
    // 1. Progressive Image Preloader for 55 Photorealistic Frames
    // -------------------------------------------------------------
    const frames: (HTMLImageElement | null)[] = new Array(TOTAL_STIR_FRAMES).fill(null);
    let framesLoadedCount = 0;
    let posterImg: HTMLImageElement | null = new window.Image();
    posterImg.src = "/stir_poster.jpg";

    const loadSingleFrame = (index: number): Promise<HTMLImageElement> => {
      return new Promise((resolve) => {
        const img = new window.Image();
        img.src = `/stir_frames/frame_${String(index).padStart(3, "0")}.webp`;
        img.onload = () => {
          frames[index] = img;
          framesLoadedCount++;
          // Draw first frame immediately when available
          if (index === 0 && !renderedAny) {
            drawCurrentFrame(0);
          }
          resolve(img);
        };
        img.onerror = () => {
          // Fallback to poster if specific frame fails
          frames[index] = posterImg;
          resolve(posterImg as HTMLImageElement);
        };
      });
    };

    // Load keyframes first (strides of 5 across the 55 frames), then remaining in background
    const keyIndices: number[] = [];
    for (let i = 0; i < TOTAL_STIR_FRAMES; i += 5) keyIndices.push(i);
    if (!keyIndices.includes(TOTAL_STIR_FRAMES - 1)) keyIndices.push(TOTAL_STIR_FRAMES - 1);

    const remainingIndices: number[] = [];
    for (let i = 0; i < TOTAL_STIR_FRAMES; i++) {
      if (!keyIndices.includes(i)) remainingIndices.push(i);
    }

    // Step 1: load frame 0 immediately
    loadSingleFrame(0).then(() => {
      // Step 2: load keyframes
      Promise.all(keyIndices.map(loadSingleFrame)).then(() => {
        // Step 3: load remaining frames progressively
        remainingIndices.forEach(loadSingleFrame);
      });
    });

    // -------------------------------------------------------------
    // 2. High-Performance Canvas Rendering (Object-fit: cover)
    // -------------------------------------------------------------
    let renderedAny = false;
    let lastRenderedFrame = -1;

    const resizeCanvas = () => {
      const rect = canvas.getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const targetW = Math.round(rect.width * dpr);
      const targetH = Math.round(rect.height * dpr);

      if (canvas.width !== targetW || canvas.height !== targetH) {
        canvas.width = targetW;
        canvas.height = targetH;
        lastRenderedFrame = -1; // force re-render
      }
    };

    const drawCurrentFrame = (frameIdx: number) => {
      if (frameIdx === lastRenderedFrame && renderedAny) return;

      // Find loaded frame (either exact frame, or nearest loaded keyframe, or poster)
      let img = frames[frameIdx];
      if (!img || !img.complete) {
        // Find nearest loaded frame
        for (let offset = 1; offset < TOTAL_STIR_FRAMES; offset++) {
          if (frameIdx - offset >= 0 && frames[frameIdx - offset]?.complete) {
            img = frames[frameIdx - offset];
            break;
          }
          if (frameIdx + offset < TOTAL_STIR_FRAMES && frames[frameIdx + offset]?.complete) {
            img = frames[frameIdx + offset];
            break;
          }
        }
      }
      if (!img || !img.complete) {
        img = frames[0] || posterImg;
      }

      if (!img || !img.complete || img.naturalWidth === 0) return;

      const cw = canvas.width;
      const ch = canvas.height;
      const iw = img.naturalWidth;
      const ih = img.naturalHeight;

      // Calculate object-fit: cover
      const scale = Math.max(cw / iw, ch / ih);
      const dw = iw * scale;
      const dh = ih * scale;
      const dx = (cw - dw) / 2;
      const dy = (ch - dh) / 2;

      ctx.drawImage(img, dx, dy, dw, dh);
      lastRenderedFrame = frameIdx;
      renderedAny = true;
    };

    resizeCanvas();
    window.addEventListener("resize", resizeCanvas);

    // -------------------------------------------------------------
    // 3. Scroll Scrubbing Animation Frame Loop
    // -------------------------------------------------------------
    let animId = 0;
    let isIntersecting = false;
    let smoothedProgress = -1;
    let lastChapter = 0;
    let lastTime = performance.now();

    const updateFrame = (now: number) => {
      const delta = Math.min((now - lastTime) / 1000, 0.05);
      lastTime = now;

      const vh = window.innerHeight;
      const vw = window.innerWidth;
      const rawProgress = clamp(
        -sec.getBoundingClientRect().top / (sec.offsetHeight - vh)
      );

      smoothedProgress =
        smoothedProgress < 0 || reduced
          ? rawProgress
          : lerp(smoothedProgress, rawProgress, 1 - Math.exp(-delta * 12));

      const p = smoothedProgress;

      // 1. Arched clip-path expands smoothly into full viewport
      const curve = easeInOutCubic(norm(p, 0, 0.28));
      const s = lerp(vw < 860 ? 24 : 35, 0, curve);
      const c = lerp(36, 0, curve);
      const u = ((vw * (100 - s * 2)) / 100 / 2) * (1 - norm(curve, 0.5, 1));
      clipDiv.style.clipPath = `inset(${c}% ${s}% 0 ${s}% round ${u}px ${u}px 0 0)`;

      // 2. Map scroll progress p to stirring frame index (0..54)
      // When scrolling forward: ladle stirs into the mixture, steam rises, camera zooms in
      // When scrolling backward: frameIndex decreases, perfectly reversing the stirring stroke
      if (reduced) {
        drawCurrentFrame(27); // static midpoint frame for reduced motion (27 of 55)
      } else {
        const frameIdx = Math.min(
          TOTAL_STIR_FRAMES - 1,
          Math.max(0, Math.floor(p * TOTAL_STIR_FRAMES))
        );
        drawCurrentFrame(frameIdx);
      }

      // 3. Header fade
      header.style.opacity = String(1 - norm(p, 0.04, 0.2));
      header.style.transform = `translate3d(0, ${-norm(p, 0, 0.22) * 60}px, 0)`;

      // 4. Scrim & chapter copy transitions
      scrim.style.opacity = String(norm(p, 0.2, 0.32));
      copy.style.opacity = String(norm(p, 0.25, 0.33));
      copy.style.transform = `translate3d(0, ${(1 - norm(p, 0.25, 0.36)) * 28}px, 0)`;

      // 5. Rotating Heritage Seal
      const sealNorm = norm(p, 0.22, 0.34);
      seal.style.opacity = String(sealNorm);
      seal.style.transform = `scale(${lerp(1.25, 1, easeInOutCubic(sealNorm))}) rotate(${lerp(
        -14,
        0,
        easeInOutCubic(sealNorm)
      )}deg)`;
      sealSvg.style.transform = `rotate(${p * 240}deg)`;

      // 6. Floating Artisan Portrait Card Parallax
      const cardNorm = norm(p, 0.48, 0.97);
      const cardCurve =
        cardNorm < 0.5
          ? 0.5 * easeInOutCubic(cardNorm * 2)
          : 0.5 + 0.5 * easeInOutCubic((cardNorm - 0.5) * 2);
      const cardScale = Math.sin(cardCurve * Math.PI);
      const cardY = lerp(vh * 0.95, -vh * 1.05, cardNorm * 0.35 + cardCurve * 0.65);

      cardDiv.style.transform = `translate3d(0, ${cardY}px, 0) rotate(${lerp(
        7,
        -4,
        cardCurve
      )}deg) scale(${lerp(0.9, 1, cardScale)})`;
      cardImg.style.transform = `translate3d(0, ${lerp(-14, 0, cardCurve)}%, 0)`;

      // 7. Active chapter tracking
      let currentChap = 0;
      for (
        ;
        currentChap < chapters.length - 1 && p >= chapters[currentChap + 1].start;
      ) {
        currentChap++;
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
      { rootMargin: "25% 0px" }
    );

    observer.observe(sec);
    updateFrame(performance.now());

    return () => {
      isIntersecting = false;
      cancelAnimationFrame(animId);
      observer.disconnect();
      window.removeEventListener("resize", resizeCanvas);
    };
  }, [chapters]);

  return (
    <section
      id="heritage"
      ref={sectionRef}
      className="relative h-[400vh] bg-[#0A241E] text-[#F7F1E5]"
    >
      <div className="sticky top-0 h-svh min-h-[540px] overflow-hidden">
        {/* Expanding Arched Background View with Scroll-Controlled Sweet-Making Animation */}
        <div
          ref={clipDivRef}
          className="absolute inset-0 will-change-[clip-path]"
        >
          {/* Scroll-Scrubbable Photorealistic Stirring Canvas */}
          <canvas
            ref={canvasRef}
            aria-label="Photorealistic traditional sweet maker stirring rich golden sweet mixture in a traditional brass pan over a wood-fired stove at Sri Amman Bakery, controlled by scroll progress"
            className="block h-full w-full object-cover will-change-transform"
          >
            {/* Fallback image if canvas is unsupported */}
            <img
              src="/stir_poster.jpg"
              alt="Traditional sweet artisans crafting sweets in 100% pure homemade ghee"
              className="block h-full w-full object-cover"
            />
          </canvas>

          {/* Atmospheric Shadow Scrim */}
          <div
            ref={scrimRef}
            aria-hidden="true"
            className="estate-scrim absolute inset-0 opacity-0 pointer-events-none"
          />
        </div>

        {/* Top Centered Section Heading */}
        <div
          ref={headerRef}
          className="absolute inset-x-(--pad) top-[clamp(100px,15vh,150px)] text-center pointer-events-none"
        >
          <h2 className="font-serif text-[clamp(2.3rem,4.5vw,4.6rem)] leading-[1.02] font-medium tracking-[-.015em] text-balance">
            {siteConfig.estate.heading}{" "}
            <em className="font-normal text-[#C99732]">
              {siteConfig.estate.accent}
            </em>
          </h2>
          <p className="mt-[clamp(12px,2vh,20px)] text-[.7rem] font-normal tracking-[.3em] text-[#C99732]/85 uppercase">
            {siteConfig.estate.subheading}
          </p>
        </div>

        {/* Floating Artisan Portrait Card */}
        <div
          ref={cardDivRef}
          aria-hidden="true"
          className="absolute top-[calc(50%-min(16.5vw,225px))] right-[calc(var(--pad)+var(--seal)+3vw)] aspect-[2/3] w-[min(22vw,300px)] overflow-hidden rounded-[18px] border border-[#C99732]/40 shadow-[0_40px_70px_-30px_rgba(7,27,22,.9)] will-change-transform max-[860px]:top-[16%] max-[860px]:right-[6vw] max-[860px]:w-[42vw] pointer-events-none"
        >
          <Image
            ref={cardImgRef}
            src="/artisan_craft.jpg"
            alt="Master sweet artisan shaping golden laddus"
            width={1000}
            height={1500}
            className="block h-[116%] w-full max-w-none object-cover will-change-transform"
          />
        </div>

        {/* Rotating Circular Heritage Brass Seal */}
        <div
          ref={sealRef}
          role="img"
          aria-label={siteConfig.estate.sealText}
          className="estate-seal absolute right-(--pad) bottom-[clamp(36px,8vh,88px)] size-(--seal) opacity-0 will-change-transform max-[860px]:top-[13%] max-[860px]:right-auto max-[860px]:bottom-auto max-[860px]:left-(--pad) pointer-events-none"
        >
          <svg
            ref={sealSvgRef}
            viewBox="0 0 200 200"
            aria-hidden="true"
            className="absolute inset-0 size-full"
          >
            <defs>
              <path
                id="estate-seal-ring"
                d="M100 100m-82 0a82 82 0 1 1 164 0a82 82 0 1 1 -164 0"
              />
            </defs>
            <text className="fill-[#C99732] font-sans text-[10px] font-medium tracking-widest uppercase">
              <textPath
                href="#estate-seal-ring"
                textLength={SEAL_CIRCUMFERENCE}
                lengthAdjust="spacing"
              >
                {siteConfig.estate.sealText}
              </textPath>
            </text>
          </svg>

          {/* Inner Sweet Photo inside Seal */}
          <Image
            src="/seal_sweet.jpg"
            alt="Pure homemade ghee golden laddu"
            width={554}
            height={554}
            className="absolute inset-[19%] block size-[62%] rounded-full border border-[#C99732]/60 object-cover"
          />
        </div>

        {/* Sequential Heritage Chapters */}
        <div
          ref={copyRef}
          className="absolute bottom-[clamp(36px,8vh,88px)] left-(--pad) w-[min(34rem,calc(100%-var(--pad)*2))] opacity-0 max-[860px]:bottom-7 pointer-events-none"
        >
          <div className="grid">
            {chapters.map((chap, idx) => {
              const state =
                idx === activeChapter
                  ? "active"
                  : idx < activeChapter
                  ? "past"
                  : "ahead";
              return (
                <article
                  key={chap.title}
                  className="chapter"
                  data-state={state}
                  aria-hidden={idx !== activeChapter}
                >
                  <h3 className="font-serif text-[clamp(2.3rem,4.5vw,4.6rem)] leading-[1.02] font-medium tracking-[-.015em] max-[860px]:text-[clamp(1.9rem,8.4vw,2.8rem)]">
                    {chap.title}{" "}
                    <em className="block font-normal text-[#C99732]">
                      {chap.accent}
                    </em>
                  </h3>
                  <p className="mt-[clamp(14px,2.2vh,24px)] max-w-[36ch] text-[clamp(.95rem,1.12vw,1.12rem)] text-[#F7F1E5]/85 max-[860px]:mt-3 max-[860px]:text-[.92rem] max-[860px]:leading-normal">
                    {chap.body}
                  </p>
                </article>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
};
