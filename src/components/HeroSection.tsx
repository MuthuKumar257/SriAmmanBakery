"use client";

import React, { useEffect, useRef } from "react";
import Image from "next/image";
import * as THREE from "three";
import { siteConfig } from "@/config/site";
import { DRIP_SVG_PATH, PL, SL } from "@/lib/dripMath";
import { clamp, lerp, prefersReducedMotion } from "@/lib/utils";

interface HeroSectionProps {
  heroRef: React.RefObject<HTMLElement | null>;
  slotRef: React.RefObject<HTMLDivElement | null>;
  active: boolean;
}

// Scalloped SVG drip edge
const DripEdge: React.FC = () => {
  return (
    <div
      data-drip-edge=""
      aria-hidden="true"
      className="pointer-events-none absolute inset-x-0 top-1/2 bottom-0"
    >
      <svg
        className="drip-svg"
        viewBox={`0 0 ${SL} 450`}
      >
        <path
          className="drip-path animate-drip-flow"
          d={DRIP_SVG_PATH}
        />
      </svg>
    </div>
  );
};

// Teardrop Lathe Geometry for liquid droplet
function createDropletGeometry(): THREE.LatheGeometry {
  const points: THREE.Vector2[] = [];
  const t = Math.PI / 5;
  for (let n = 0; n <= 14; n++) {
    const r = lerp(-Math.PI / 2, t, n / 14);
    points.push(new THREE.Vector2(Math.cos(r), Math.sin(r)));
  }
  const [n, r] = [Math.cos(t), Math.sin(t)];
  for (let step = 1; step <= 12; step++) {
    const i = step / 12;
    points.push(
      new THREE.Vector2(n * Math.pow(1 - i, 1.6), r + (2.7 - r) * Math.pow(i, 0.9))
    );
  }
  return new THREE.LatheGeometry(points, 28);
}

interface Droplet {
  tip: { x: number; y: number; r: number };
  r: number;
  y: number;
  vy: number;
  age: number;
  hang: number;
  falling: boolean;
}

// Three.js Glistening Pure Homemade Ghee / Saffron Droplet Simulator
const DropletCanvas: React.FC<{
  heroRef: React.RefObject<HTMLElement | null>;
  active: boolean;
}> = ({ heroRef, active }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const activeRef = useRef(active);

  useEffect(() => {
    activeRef.current = active;
  }, [active]);

  useEffect(() => {
    const container = containerRef.current;
    const heroEl = heroRef.current;
    if (!container || !heroEl || prefersReducedMotion()) return;

    let renderer: THREE.WebGLRenderer;
    try {
      renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    } catch {
      return;
    }

    renderer.setClearColor(0x000000, 0);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    const domElement = renderer.domElement;
    domElement.className = "block h-full w-full";
    container.appendChild(domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.OrthographicCamera(0, 1, 0, -1, -2000, 2000);
    camera.position.z = 1000;

    // Warm golden lights for liquid pure homemade ghee / saffron drops
    const keyLight = new THREE.DirectionalLight(0xffdf8e, 2.8);
    keyLight.position.set(-0.55, 0.75, 1);
    const rimLight = new THREE.DirectionalLight(0xc99732, 0.9);
    rimLight.position.set(0.9, -0.3, 0.6);
    const ambientLight = new THREE.AmbientLight(0x0e362c, 1.2);
    scene.add(keyLight, rimLight, ambientLight);

    // Warm glistening ghee droplet material with heritage gold tone
    const material = new THREE.MeshPhysicalMaterial({
      color: 0xc99732,
      roughness: 0.18,
      clearcoat: 1.0,
      clearcoatRoughness: 0.1,
      transmission: 0.3,
      thickness: 1.2,
    });

    const maxDrops = 90;
    const geometry = createDropletGeometry();
    const instancedMesh = new THREE.InstancedMesh(geometry, material, maxDrops);
    instancedMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    instancedMesh.frustumCulled = false;
    instancedMesh.count = 0;
    scene.add(instancedMesh);

    const droplets: Droplet[] = [];
    let tipPositions: { x: number; y: number; r: number }[] = [];
    let clientW = 1;
    let clientH = 1;
    let gravity = 1500;
    let timeAccum = 0;
    let spawnTimer = 0;
    let initialBursts = 4;

    const handleResize = () => {
      clientW = container.clientWidth;
      clientH = container.clientHeight;
      gravity = 1650 * clamp(clientH / 900, 0.7, 1.4);

      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
      renderer.setSize(clientW, clientH, false);
      camera.right = clientW;
      camera.bottom = -clientH;
      camera.updateProjectionMatrix();

      const svgEl = heroEl.querySelector<SVGElement>("[data-drip-edge] svg");
      const dripEdgeEl = heroEl.querySelector<HTMLElement>("[data-drip-edge]");
      if (!svgEl || !dripEdgeEl) return;

      const svgRect = svgEl.getBoundingClientRect();
      const heroRect = heroEl.getBoundingClientRect();
      const scale = svgRect.height / 450;
      const leftOffset = svgRect.left - heroRect.left;

      tipPositions = [-1, 0, 1]
        .flatMap((offset) =>
          PL.map((t) => ({
            x: leftOffset + (t.x + offset * SL) * scale,
            y: dripEdgeEl.offsetTop + t.y * scale,
            r: t.r * scale,
          }))
        )
        .filter((t) => t.x > 8 && t.x < clientW - 8);
    };

    const spawnDroplet = () => {
      const candidates = tipPositions.filter(
        (tip) => !droplets.some((d) => d.tip === tip && !d.falling)
      );
      if (!candidates.length || droplets.length >= maxDrops) return;
      const chosen = candidates[Math.floor(Math.random() * candidates.length)];
      droplets.push({
        tip: chosen,
        r: clamp(chosen.r * (0.28 + Math.random() * 0.14), 3.5, 10.5),
        y: chosen.y,
        vy: 0,
        age: 0,
        hang: initialBursts > 0 ? 0.2 + Math.random() * 0.35 : 0.45 + Math.random() * 0.75,
        falling: false,
      });
    };

    const updatePhysics = (delta: number) => {
      timeAccum += delta;
      if (timeAccum < 1.1) return;

      spawnTimer -= delta;
      while (spawnTimer <= 0) {
        spawnDroplet();
        spawnTimer += initialBursts-- > 0 ? 0 : 0.07 + Math.random() * 0.16;
      }

      for (let i = droplets.length - 1; i >= 0; i--) {
        const d = droplets[i];
        if (d.falling) {
          d.vy += gravity * delta;
          d.y += d.vy * delta;
          if (d.y - d.r * 6 > clientH) {
            droplets.splice(i, 1);
          }
        } else {
          d.age += delta;
          if (d.age >= d.hang) {
            d.falling = true;
            d.vy = 30;
          }
        }
      }
    };

    const dummy = new THREE.Object3D();
    const pos = new THREE.Vector3();
    const scale = new THREE.Vector3();
    const rot = new THREE.Quaternion();

    const renderScene = () => {
      droplets.forEach((d, i) => {
        if (d.falling) {
          scale.set(d.r, d.r * 1.25 * clamp(1 + d.vy / 1300, 1, 1.8), d.r);
        } else {
          const t = d.age / d.hang;
          const curve = t * t * (3 - 2 * t);
          const r = d.r * lerp(0.35, 1, curve);
          d.y = d.tip.y + d.r * lerp(-0.7, 0.55, curve);
          scale.set(r, r * lerp(0.7, 1.25, curve), r);
        }
        pos.set(d.tip.x, -d.y, 0);
        dummy.position.copy(pos);
        dummy.quaternion.copy(rot);
        dummy.scale.copy(scale);
        dummy.updateMatrix();
        instancedMesh.setMatrixAt(i, dummy.matrix);
      });

      instancedMesh.count = droplets.length;
      instancedMesh.instanceMatrix.needsUpdate = true;
      renderer.render(scene, camera);
    };

    let animId = 0;
    let isDisposed = false;
    let lastTime = performance.now();

    const animate = (currentTime: number) => {
      const delta = Math.min((currentTime - lastTime) / 1000, 0.05);
      lastTime = currentTime;

      if (activeRef.current && window.scrollY < heroEl.offsetTop + heroEl.offsetHeight) {
        updatePhysics(delta);
        renderScene();
      }
      animId = requestAnimationFrame(animate);
    };

    handleResize();
    window.addEventListener("resize", handleResize);
    document.fonts?.ready.then(() => !isDisposed && handleResize());
    animId = requestAnimationFrame(animate);

    return () => {
      isDisposed = true;
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", handleResize);
      geometry.dispose();
      material.dispose();
      renderer.dispose();
      domElement.remove();
    };
  }, [heroRef]);

  return (
    <div
      ref={containerRef}
      aria-hidden="true"
      className="pointer-events-none absolute inset-0 z-[2] [mask-image:linear-gradient(to_bottom,#000_86%,transparent_99%)]"
    />
  );
};

export const HeroSection: React.FC<HeroSectionProps> = ({
  heroRef,
  slotRef,
  active,
}) => {
  const gradientTextClass =
    "bg-linear-to-b from-[#FFFFFF] from-15% via-[#F7F1E5] via-55% to-[#C99732] to-95% bg-clip-text px-[.04em] pt-[.08em] pb-[.14em] text-transparent";

  return (
    <section
      id="top"
      ref={heroRef}
      className="hero-bg relative h-svh min-h-[540px] overflow-hidden"
    >
      {/* Golden Scalloped Drip Edge */}
      <DripEdge />

      {/* Main Brand Title ("Sri Amman" & "Bakery") with Perfectly Symmetric Zero-Overlap Alignment */}
      <h1 className="absolute inset-x-0 top-[44%] z-[1] -translate-y-1/2 [opacity:var(--hero-fade,1)] max-[860px]:top-[18%]">
        {/* Desktop View (> 860px): 3-Column Symmetric Layout with Guaranteed Centerpiece Clearance */}
        <div className="hidden min-[861px]:grid min-[861px]:grid-cols-[1fr_auto_1fr] min-[861px]:items-center w-full px-(--pad)">
          {/* Left Column: "Sri Amman" right-aligned with guaranteed clearance */}
          <div className="flex justify-end pr-[clamp(16px,2.2vw,36px)]">
            <span
              className={`${gradientTextClass} animate-rise font-serif text-[clamp(2.4rem,5.2vw,6.5rem)] leading-none font-medium tracking-[-.02em] whitespace-nowrap`}
            >
              {siteConfig.hero.titleWord1}
            </span>
          </div>

          {/* Center Column: Dedicated Spacer exactly matching the platter width */}
          <div
            aria-hidden="true"
            className="w-(--cup) shrink-0 pointer-events-none"
          />

          {/* Right Column: "Bakery" left-aligned with identical clearance */}
          <div className="flex justify-start pl-[clamp(16px,2.2vw,36px)]">
            <span
              className={`${gradientTextClass} animate-rise-late font-serif text-[clamp(2.4rem,5.2vw,6.5rem)] leading-none font-normal italic tracking-[-.02em] whitespace-nowrap`}
            >
              {siteConfig.hero.titleWord2}
            </span>
          </div>
        </div>

        {/* Mobile View (<= 860px): Centered single title cleanly above the platter */}
        <div className="flex min-[861px]:hidden justify-center items-center gap-[.25em] px-4 font-serif text-[clamp(1.8rem,7.8vw,3.2rem)] leading-none font-medium tracking-[-.02em] whitespace-nowrap">
          <span className={`${gradientTextClass} animate-rise`}>
            {siteConfig.hero.titleWord1}
          </span>
          <span className={`${gradientTextClass} animate-rise-late font-normal italic`}>
            {siteConfig.hero.titleWord2}
          </span>
        </div>
      </h1>

      {/* Three.js Droplet Simulation */}
      <DropletCanvas heroRef={heroRef} active={active} />

      {/* Centerpiece Hero Sweet */}
      <div
        ref={slotRef}
        aria-hidden="true"
        className="pointer-events-none absolute top-[44%] left-1/2 z-[2] aspect-square w-(--cup) -translate-x-1/2 -translate-y-1/2 max-[860px]:top-[50%]"
      >
        <Image
          src="/sweet.png"
          alt={`${siteConfig.brandName} Handcrafted Sweets`}
          width={1254}
          height={1254}
          priority
          className="relative block h-full w-full animate-cup-in object-contain filter drop-shadow-[0_25px_40px_rgba(7,27,22,0.85)]"
        />
      </div>

      {/* Bottom Hero Description & Heritage Stat */}
      <div className="absolute inset-x-(--pad) bottom-[clamp(22px,4.5vh,48px)] z-[3] grid animate-fade-up grid-cols-2 items-end gap-6 [opacity:var(--hero-fade,1)] max-[860px]:grid-cols-[1fr_auto] max-[860px]:gap-4">
        <p className="max-w-[30ch] text-[clamp(.9rem,1.05vw,1.05rem)] text-[#F7F1E5]/80 max-[860px]:max-w-[26ch] max-[860px]:text-[.86rem]">
          {siteConfig.hero.blurb}
        </p>

        <p className="flex items-end gap-3.5 justify-self-end text-[.68rem] leading-[1.7] font-normal tracking-[.24em] text-[#F7F1E5]/75 uppercase">
          <strong className="font-serif text-[clamp(3rem,5.4vw,5.2rem)] leading-[.8] font-normal tracking-[-.02em] text-[#C99732]">
            {siteConfig.hero.statNumber}
          </strong>
          <span className="max-[860px]:text-[.6rem] max-[860px]:leading-tight">
            {siteConfig.hero.statLabel.split(" ").slice(0, 2).join(" ")}
            <br />
            {siteConfig.hero.statLabel.split(" ").slice(2).join(" ")}
          </span>
        </p>
      </div>
    </section>
  );
};

