# Sri Amman Bakery

> **Serving sweetness since 2022**  
> Founded by **Mangalasamy P**

A premium, interactive web experience celebrating the artisanal heritage of **Sri Amman Bakery**. Built with Next.js 15, React 19, Tailwind CSS, Three.js, and canvas scroll-scrubbed cinematography.

---

## Brand Identity & Heritage

Sri Amman Bakery was established in 2022 under the vision of founder **Mangalasamy P**. Every confection is handcrafted with **100% Pure Homemade Ghee**, slow-simmered in traditional brass kadais over glowing firewood hearths, and served fresh daily.

### Authoritative Brand Palette
Inspired directly by the Sri Amman Bakery emblem:
- **Deep Forest Green** (`#123D32`): Navigation header, hero backgrounds, primary actions, and footer.
- **Deep Maroon** (`#651B24`): Major headings, highlights, and selective typographical emphasis.
- **Heritage Gold** (`#C99732`): Filigree borders, divider accents, icons, and animation highlights.
- **Warm Ivory** (`#F7F1E5`): Spacious background canvas and product showcase cards.

---

## Key Features

### 1. Scroll-Driven 55-Frame Kadai Stirring Animation
- Replaced static imagery with a photorealistic sequence of a sweet artisan stirring traditional sweet mixture in a large brass kadai over glowing wood embers.
- Scrubbable in real time: scrolling down advances the stirring ladle and heat waves, while scrolling up reverses smoothly.
- Optimized 55 WebP frames (`public/stir_frames/`) rendered on an HTML5 `<canvas>` via GSAP ScrollTrigger with responsive pixel-ratio scaling and memory cleanup.

### 2. Signature 12-Sweet Showcase Grid
Clicking any sweet card opens an informational description modal detailing the authentic texture, taste notes, and heritage ingredients (strictly informational with **zero purchasing controls**):

1. **Laddu** – Golden spheres of gram flour, dry fruits, and homemade ghee.
2. **Mysore Pak** – Porous, melt-in-the-mouth royal confection.
3. **Jalebi** – Crisp, golden spirals soaked in fragrant saffron syrup.
4. **Badam Burfi** – Rich, velvety almond fudge garnished with silver leaf.
5. **Boost Burfi** – Nostalgic malted chocolate-flavored milk fudge.
6. **Horlicks Burfi** – Creamy, golden malt-infused sweet confectionery.
7. **Badusha** – Flaky, layered glazed pastry with a tender crumb.
8. **Carrot Burfi** – Slow-cooked fresh carrots with whole milk, cardamom, and ghee.
9. **Pista Burfi** – Pure pistachio fudge enriched with slivered nuts.
10. **Rose Burfi** – Delicate, aromatic confection infused with damask rose essence.
11. **Gulab Jamun** – Soft, golden milk-solid dumplings soaked in rose-cardamom syrup.
12. **Milk Laddu** (*Also called Tirupathi Laddu*) – Traditional rich, soft milk laddu adorned with dry fruits.

### 3. Precision Responsive Hero Section
- 3-column symmetric layout with calibrated clearances between the title "Sri Amman Bakery" and the floating centerpiece brass tray.
- Dynamic syrup dripping illustration and warm lighting effects.
- Tested and verified on ultra-wide desktop, tablet, and mobile screens.

### 4. 100% Pure Brand Compliance
- Strict English typography throughout (zero Hindi or foreign script transliterations).
- Tagline standard: strictly **"100% Pure Homemade Ghee"**.
- Pure brand showcase: all purchasing options, cart triggers, and WhatsApp ordering flows have been omitted in favor of storytelling.

---

## Tech Stack

- **Framework**: [Next.js 15](https://nextjs.org/) (App Router, Turbopack)
- **UI Library**: [React 19](https://react.dev/)
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com/)
- **Animations**: [GSAP](https://gsap.com/) (ScrollTrigger) & [Framer Motion](https://www.framer.com/motion/)
- **Graphics**: [Three.js](https://threejs.org/) & Canvas 2D
- **Icons**: [Lucide React](https://lucide.dev/)
- **Language**: TypeScript

---

## Getting Started

### Prerequisites
- Node.js 18.18.0 or newer
- npm or yarn

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MuthuKumar257/SriAmmanBakery.git
   cd SriAmmanBakery
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```
   Open [http://localhost:3000](http://localhost:3000) in your browser.

4. Build for production:
   ```bash
   npm run build
   npm run start
   ```

---

## Directory Structure

```plaintext
SriAmmanBakery/
├── public/
│   ├── sweets/             # Standardized 800x600 high-res photography of all 12 sweets
│   ├── stir_frames/        # 55 WebP frames of scroll-scrubbable kadai stirring
│   ├── logo.png            # Authoritative Sri Amman Bakery identity logo
│   ├── sweet_tray.png      # Hero centerpiece sweet platter
│   └── favicon.ico         # Optimized multi-layer browser icon
├── src/
│   ├── app/
│   │   ├── globals.css     # Brand color tokens & custom utility styling
│   │   ├── layout.tsx      # Root metadata & font declarations
│   │   └── page.tsx        # Homepage composing all sections
│   ├── components/
│   │   ├── HeroSection.tsx # Balanced 3-column hero layout
│   │   ├── EstateSection.tsx # Canvas 55-frame stirring engine
│   │   ├── SweetsShowcase.tsx # Responsive 12-sweet showcase grid
│   │   ├── OrderModal.tsx  # Informational product detail modal
│   │   ├── HeritageSection.tsx # Our Story & founder Mangalasamy P (2022)
│   │   ├── GiftBoxSection.tsx # Packaging craftsmanship showcase
│   │   ├── FloatingDosa.tsx # Interactive visual elements
│   │   └── Footer.tsx      # Brand footer
├── scripts/                # Audit, verification, and image optimization tooling
├── package.json
└── README.md
```

---

## License

© 2022–Present Sri Amman Bakery. Handcrafted with pride.

