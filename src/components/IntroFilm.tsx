"use client";

import React, { useEffect, useRef, useState } from "react";
import Image from "next/image";
import { siteConfig } from "@/config/site";

interface IntroFilmProps {
  onReveal: () => void;
  onDone: () => void;
}

const INTRO_DURATION_MS = 4800;
const REVEAL_DURATION_MS = 1300;
const PLAYBACK_RATE = 1.3;
const SOFT_EASE = "cubic-bezier(.22,.7,.2,1)";

export const IntroFilm: React.FC<IntroFilmProps> = ({ onReveal, onDone }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const logoRef = useRef<HTMLImageElement>(null);
  const [phase, setPhase] = useState<"wait" | "title" | "reveal">("wait");
  const [logoTransform, setLogoTransform] = useState<string>("");

  useEffect(() => {
    const video = videoRef.current;
    const proceedToTitle = () => {
      setPhase((p) => (p === "wait" ? "title" : p));
    };

    if (video) {
      video.addEventListener("playing", proceedToTitle);
      video.defaultPlaybackRate = video.playbackRate = PLAYBACK_RATE;
      video.play().catch(() => {
        // Autoplay may be restricted; fallback timer will proceed
      });
    }

    // Safety timeout in case video loading is slow
    const fallbackTimer = window.setTimeout(proceedToTitle, 1500);

    return () => {
      video?.removeEventListener("playing", proceedToTitle);
      window.clearTimeout(fallbackTimer);
    };
  }, []);

  // Phase transition: title -> reveal
  useEffect(() => {
    if (phase !== "title") return;
    const timer = window.setTimeout(() => setPhase("reveal"), INTRO_DURATION_MS);
    return () => window.clearTimeout(timer);
  }, [phase]);

  // Reveal transition: compute nav logo position and translate center logo
  useEffect(() => {
    if (phase !== "reveal") return;

    const logoEl = logoRef.current;
    const navLogoEl = document.querySelector<HTMLElement>("[data-nav-logo]");

    if (logoEl && navLogoEl) {
      const navRect = navLogoEl.getBoundingClientRect();
      const deltaX = navRect.left - logoEl.offsetLeft;
      const deltaY = navRect.top - logoEl.offsetTop;
      const scale = navRect.width / logoEl.offsetWidth;

      setLogoTransform(`translate3d(${deltaX}px, ${deltaY}px, 0) scale(${scale})`);
    }

    onReveal();

    const doneTimer = window.setTimeout(onDone, 1380);
    return () => window.clearTimeout(doneTimer);
  }, [phase, onReveal, onDone]);

  const isTitle = phase === "title";
  const isReveal = phase === "reveal";

  const logoStyle: React.CSSProperties = isReveal
    ? {
        opacity: 1,
        transform: logoTransform || "none",
        transformOrigin: "0 0",
        transition: `transform ${REVEAL_DURATION_MS}ms cubic-bezier(.76,0,.24,1)`,
      }
    : isTitle
    ? {
        opacity: 1,
        transform: "none",
        transition: `opacity 1.4s ease .7s, transform 2.6s ${SOFT_EASE} .7s`,
      }
    : {
        opacity: 0,
        transform: "scale(.9)",
      };

  const textStyle = (delay: number): React.CSSProperties => ({
    opacity: isTitle ? 1 : 0,
    transition: isTitle
      ? `opacity 1.4s ease ${delay}s, letter-spacing 2.6s ${SOFT_EASE} ${delay}s`
      : "opacity .5s ease",
  });

  return (
    <div
      data-film=""
      className={`fixed inset-0 z-50 ${isReveal ? "pointer-events-none" : ""}`}
    >
      {/* Background Video / Atmosphere */}
      <div
        className="absolute inset-0 overflow-hidden bg-black transition-opacity duration-[1200ms] ease-in-out"
        style={{ opacity: isReveal ? 0 : 1 }}
      >
        <video
          ref={videoRef}
          src="/drone zoom.mp4"
          muted
          playsInline
          autoPlay
          preload="auto"
          aria-hidden="true"
          className="absolute inset-0 size-full object-cover transition-opacity duration-[1600ms]"
          style={{ opacity: phase === "wait" ? 0 : 1 }}
        />
        <div className="intro-grade absolute inset-0" />
      </div>

      {/* Intro Overlay Content */}
      <div className="absolute inset-0 flex flex-col items-center justify-center px-(--pad) text-center">
        {/* Kicker with heritage gold horizontal divider lines */}
        <p
          style={{
            ...textStyle(0.2),
            letterSpacing: isTitle ? ".5em" : ".9em",
          }}
          className="flex items-center gap-5 indent-[.5em] text-[.72rem] font-normal whitespace-nowrap text-[#C99732] uppercase before:h-px before:w-[clamp(20px,5vw,64px)] before:bg-[#C99732]/60 after:h-px after:w-[clamp(20px,5vw,64px)] after:bg-[#C99732]/60 max-[860px]:text-[.62rem]"
        >
          {siteConfig.intro.kicker}
        </p>

        {/* Center Big Logo */}
        <Image
          ref={logoRef}
          src="/logo.png"
          alt={siteConfig.brandName}
          width={862}
          height={688}
          priority
          style={logoStyle}
          className="my-[clamp(10px,2.4vh,26px)] block h-[min(40vh,58vw)] w-auto max-w-none will-change-transform"
        />

        {/* Subtitle / Quote */}
        <p
          style={textStyle(1.7)}
          className="font-serif text-[clamp(1.2rem,2vw,1.9rem)] leading-tight text-[#F7F1E5] italic"
        >
          {siteConfig.intro.subtext}
        </p>
      </div>

      {/* Skip Button */}
      <button
        type="button"
        onClick={() => setPhase("reveal")}
        className={`absolute right-(--pad) bottom-[clamp(22px,4.5vh,48px)] cursor-pointer text-[.66rem] font-normal tracking-[.3em] text-[#F7F1E5]/75 uppercase transition-[color,opacity] duration-500 hover:text-[#C99732] ${
          isReveal ? "opacity-0" : "opacity-100"
        }`}
      >
        {siteConfig.intro.skipText}
      </button>
    </div>
  );
};

