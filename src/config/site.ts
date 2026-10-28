export interface SweetProduct {
  id: string;
  name: string;
  subtitle?: string;
  weight: string;
  description: string;
  tasteAndTexture: string;
  ingredients: string[];
  shelfLife: string;
  image: string;
  badge?: string;
  category: string;
}

const SWEETS_COLLECTION: SweetProduct[] = [
  {
    id: "laddu",
    name: "Laddu",
    weight: "500 g",
    description: "Golden, round traditional Indian sweet crafted with slow-roasted gram flour, 100% pure homemade ghee, green cardamom, melon seeds, and slivered pistachios.",
    tasteAndTexture: "Melt-in-the-mouth texture with an aromatic cardamom warmth, subtle nuttiness from slow-roasted gram flour, and a gentle crunch from toasted melon seeds.",
    ingredients: ["Gram Flour", "100% Pure Homemade Ghee", "Sugar", "Melon Seeds", "Pistachios", "Green Cardamom"],
    shelfLife: "15 Days",
    image: "/sweets/laddu.jpg",
    badge: "Traditional Classic",
    category: "Gram Flour Sweet",
  },
  {
    id: "mysore-pak",
    name: "Mysore Pak",
    weight: "500 g",
    description: "Rich, golden, traditional gram-flour sweet with a porous, honeycomb crumb that melts luxuriously on the tongue.",
    tasteAndTexture: "Silky, delicate honeycomb crumb with an unmistakable caramelized ghee aroma and an instant dissolve on the palate.",
    ingredients: ["Gram Flour", "100% Pure Homemade Ghee", "Sugar", "Green Cardamom"],
    shelfLife: "20 Days",
    image: "/sweets/mysore-pak.jpg",
    badge: "100% Pure Homemade Ghee",
    category: "Heritage Specialty",
  },
  {
    id: "jalebi",
    name: "Jalebi",
    weight: "500 g",
    description: "Bright orange, syrup-soaked spiral sweet fried crisp to golden perfection and steeped in warm saffron sugar syrup.",
    tasteAndTexture: "Crisp and crunchy outer shell that bursts with warm, fragrant saffron syrup at the very first bite.",
    ingredients: ["Wheat Flour", "100% Pure Homemade Ghee", "Saffron Sugar Syrup", "Green Cardamom"],
    shelfLife: "7 Days",
    image: "/sweets/jalebi.jpg",
    badge: "Crisp & Syrup-Soaked",
    category: "Festive Spiral Sweet",
  },
  {
    id: "badam-burfi",
    name: "Badam Burfi",
    weight: "500 g",
    description: "Almond-based sweet cut into neat diamond pieces, infused with fragrant cardamom and crowned with pure edible silver foil and slivered almonds.",
    tasteAndTexture: "Soft, smooth fudge with rich nutty almond flavors, balanced sweetness, and delicate cardamom aromatics.",
    ingredients: ["Almonds", "Sugar", "100% Pure Homemade Ghee", "Green Cardamom", "Edible Silver Foil"],
    shelfLife: "20 Days",
    image: "/sweets/badam-burfi.jpg",
    badge: "Royal Almond Delicacy",
    category: "Diamond Nut Burfi",
  },
  {
    id: "boost-burfi",
    name: "Boost Burfi",
    weight: "500 g",
    description: "Chocolate-brown malt burfi with an appetizing, rich fudge texture, deep malt aroma, and crunchy embedded cashews.",
    tasteAndTexture: "Decadent chocolate-malt fudge texture with toasted cashew crunch and rich milky caramel notes.",
    ingredients: ["Boost Malt", "Milk Solids", "100% Pure Homemade Ghee", "Sugar", "Cashews"],
    shelfLife: "18 Days",
    image: "/sweets/boost-burfi.jpg",
    badge: "Signature Malt Fudge",
    category: "Malted Fudge Specialty",
  },
  {
    id: "horlicks-burfi",
    name: "Horlicks Burfi",
    weight: "500 g",
    description: "Malt-flavored burfi presented in clean, attractive square pieces with a delicate milky aroma and toasted slivered nuts.",
    tasteAndTexture: "Smooth, velvety golden crumb with comforting creamy malt sweetness and roasted nut accents.",
    ingredients: ["Horlicks Malt", "Milk Solids", "100% Pure Homemade Ghee", "Sugar", "Almonds", "Pistachios"],
    shelfLife: "18 Days",
    image: "/sweets/horlicks-burfi.jpg",
    badge: "Creamy Malted Square",
    category: "Golden Malted Specialty",
  },
  {
    id: "badusha",
    name: "Badusha",
    weight: "500 g",
    description: "A traditional Indian sweet with a golden exterior, delicate layers, and a rich, sweet finish.",
    tasteAndTexture: "Flaky, multi-layered golden crust with a soft, moist syrup-glazed interior that offers a satisfying, rich finish.",
    ingredients: ["Refined Wheat Flour", "100% Pure Homemade Ghee", "Sugar", "Green Cardamom"],
    shelfLife: "14 Days",
    image: "/sweets/badusha.jpg",
    badge: "Traditional Layered Pastry",
    category: "Layered Festive Pastry",
  },
  {
    id: "carrot-burfi",
    name: "Carrot Burfi",
    weight: "500 g",
    description: "Vibrant orange traditional sweet prepared with freshly grated garden carrots, slow-condensed milk, 100% pure homemade ghee, cardamom, and toasted cashews.",
    tasteAndTexture: "Moist, melt-in-mouth texture with natural carrot sweetness, slow-simmered milk richness, and an aromatic cardamom warmth.",
    ingredients: ["Fresh Carrots", "Milk Solids", "100% Pure Homemade Ghee", "Sugar", "Cashews", "Green Cardamom"],
    shelfLife: "10 Days",
    image: "/sweets/carrot-burfi.jpg",
    badge: "Fresh Garden Delicacy",
    category: "Fresh Carrot Confectionery",
  },
  {
    id: "pista-burfi",
    name: "Pista Burfi",
    weight: "500 g",
    description: "Luxurious pastel-green diamond burfi crafted from premium ground pistachios, condensed whole milk, pure homemade ghee, and cardamom.",
    tasteAndTexture: "Silky, delicate fudge with deep nutty pistachio aromatics, mild balanced sweetness, and an elegant melt.",
    ingredients: ["Pistachios", "Milk Solids", "100% Pure Homemade Ghee", "Sugar", "Green Cardamom"],
    shelfLife: "18 Days",
    image: "/sweets/pista-burfi.jpg",
    badge: "Royal Pistachio Delicacy",
    category: "Diamond Nut Confectionery",
  },
  {
    id: "rose-burfi",
    name: "Rose Burfi",
    weight: "500 g",
    description: "Fragrant pink confectionery infused with damask rose petals, rose water, slow-condensed milk solids, and 100% pure homemade ghee.",
    tasteAndTexture: "Delicate and velvety milk fudge carrying an enchanting floral rose fragrance and a smooth, comforting dissolve on the palate.",
    ingredients: ["Milk Solids", "100% Pure Homemade Ghee", "Sugar", "Rose Petals & Essence", "Pistachios", "Green Cardamom"],
    shelfLife: "14 Days",
    image: "/sweets/rose-burfi.jpg",
    badge: "Floral Rose Fudge",
    category: "Infused Milk Specialty",
  },
  {
    id: "gulab-jamun",
    name: "Gulab Jamun",
    weight: "500 g",
    description: "Deep golden spheres crafted from slow-reduced milk solids, gently fried in 100% pure homemade ghee and steeped in fragrant cardamom sugar syrup.",
    tasteAndTexture: "Tender, succulent, and syrup-steeped spheres that surrender luxuriously at the first bite with warm cardamom and rose aromatics.",
    ingredients: ["Milk Solids", "Wheat Flour", "100% Pure Homemade Ghee", "Sugar Syrup", "Rose Water", "Green Cardamom"],
    shelfLife: "12 Days",
    image: "/sweets/gulab-jamun.jpg",
    badge: "Classic Syrup-Soaked",
    category: "Heritage Festive Confectionery",
  },
  {
    id: "milk-laddu",
    name: "Milk Laddu",
    subtitle: "Also called Tirupathi Laddu",
    weight: "500 g",
    description: "A traditional, round Indian sweet known for its rich taste, soft texture, and delightful sweetness. A lovely choice for celebrations, family gatherings, and special occasions.",
    tasteAndTexture: "Rich, soft, and crumbly with slow-simmered milk sweetness, generous pure homemade ghee, whole cashews, plump raisins, and green cardamom.",
    ingredients: ["Milk Solids", "Gram Flour", "100% Pure Homemade Ghee", "Sugar", "Cashews", "Raisins", "Green Cardamom"],
    shelfLife: "15 Days",
    image: "/sweets/milk-laddu.jpg",
    badge: "Celebration Specialty",
    category: "Heritage Milk Laddu",
  },
];

export const siteConfig = {
  brandName: "Sri Amman Bakery",
  tagline: "Serving sweetness since 2022",
  establishedYear: "2022",
  taglineWording: "Serving sweetness since 2022",
  phoneNumber: "+91 96267 58666",
  phoneRaw: "9626758666",
  instagram: "https://www.instagram.com/sriamman_bakery/",
  whatsappChannel: "https://whatsapp.com/channel/0029Vb97jtVBadmd0d98OQ0u",
  location: "South India · Fresh Sweets & Bakes",

  // Navigation Links
  navLinks: [
    { id: "craft", label: "The Craft", shortLabel: "Craft" },
    { id: "sweets", label: "The Sweets", shortLabel: "Sweets" },
    { id: "pack", label: "The Box", shortLabel: "Box" },
    { id: "heritage", label: "Our Story", shortLabel: "Story" },
  ],

  // Intro Film Content
  intro: {
    kicker: "Sri Amman Bakery · Fresh Bakes & Sweets",
    subtext: "Serving sweetness since 2022.",
    skipText: "Skip intro",
  },

  // Hero Section
  hero: {
    titleWord1: "Sri Amman",
    titleWord2: "Bakery",
    blurb:
      "Handcrafted with 100% pure homemade ghee, slow-simmered in traditional brass pans and baked fresh daily. Serving sweetness since 2022.",
    statNumber: "2022",
    statLabel: "serving sweetness since 2022",
  },

  // The Sweets Collection with Genuine Photographs & Standardized Details (12 Sweets)
  sweets: SWEETS_COLLECTION,
  catalogue: SWEETS_COLLECTION,

  // Sweet Tray Craft Chapters (Ghee, Roast, Craft, Garnish · 01 / 04)
  craftChapters: [
    {
      label: "Ghee",
      step: "01",
      title: "Pure golden ghee,",
      accent: "as it always was.",
      body: "Slow-melted in heavy brass pans over a gentle, steady flame. It is how traditional sweets have always begun, serving sweetness since 2022.",
      start: 0,
      highlight: "100% Pure Homemade Ghee",
    },
    {
      label: "Roast",
      step: "02",
      title: "First, the",
      accent: "slow golden roast.",
      body: "Gram flour and selected malts roasted gently until aromatic and amber. The measured temperature releases deep nutty warmth and caramel aromas.",
      start: 0.2,
      highlight: "Slow-Roasted Gram Flour & Malts",
    },
    {
      label: "Craft",
      step: "03",
      title: "Then the",
      accent: "hand craftsmanship.",
      body: "Laddus rolled between experienced palms, jalebis spiraled into glistening hot pure homemade ghee, and rich burfis pressed into neat diamond cuts while perfectly warm.",
      start: 0.45,
      highlight: "Handcrafted & Cut Daily",
    },
    {
      label: "Garnish",
      step: "04",
      title: "Nuts, malt, and",
      accent: "pure edible silver foil.",
      body: "Crowned with slivered almonds, emerald pistachios, and pure edible silver foil. No artificial additives and no shortcuts. Only patience, pure ingredients, and heritage recipes.",
      start: 0.8,
      highlight: "Pure Silver Foil & Pistachios",
    },
  ],
  ritualChapters: [
    {
      label: "Ghee",
      step: "01",
      title: "Pure golden ghee,",
      accent: "as it always was.",
      body: "Slow-melted in heavy brass pans over a gentle, steady flame. It is how traditional sweets have always begun, serving sweetness since 2022.",
      start: 0,
      highlight: "100% Pure Homemade Ghee",
    },
    {
      label: "Roast",
      step: "02",
      title: "First, the",
      accent: "slow golden roast.",
      body: "Gram flour and selected malts roasted gently until aromatic and amber. The measured temperature releases deep nutty warmth and caramel aromas.",
      start: 0.2,
      highlight: "Slow-Roasted Gram Flour & Malts",
    },
    {
      label: "Craft",
      step: "03",
      title: "Then the",
      accent: "hand craftsmanship.",
      body: "Laddus rolled between experienced palms, jalebis spiraled into glistening hot pure homemade ghee, and rich burfis pressed into neat diamond cuts while perfectly warm.",
      start: 0.45,
      highlight: "Handcrafted & Cut Daily",
    },
    {
      label: "Garnish",
      step: "04",
      title: "Nuts, malt, and",
      accent: "pure edible silver foil.",
      body: "Crowned with slivered almonds, emerald pistachios, and pure edible silver foil. No artificial additives and no shortcuts. Only patience, pure ingredients, and heritage recipes.",
      start: 0.8,
      highlight: "Pure Silver Foil & Pistachios",
    },
  ],

  // Pack Section (Featured Sweet Box)
  pack: {
    heading: "Take the sweetness",
    accent: "home.",
    mobileSubtitle: "Signature Sweets Box · All 7 Heritage Varieties",
    ctaText: "Explore Collection",
    product: {
      name: "Signature Sweets Assortment Box",
      netWeight: "7 Sweets Heritage Selection (1 kg)",
      highlightsLeft: [
        "100% Pure Homemade Ghee",
        "All 7 Featured Sweets",
        "Authentic Recipe Standards",
      ],
      highlightsRight: [
        "Rich Boost & Horlicks Flavours",
        "Zero Artificial Additives",
        "Festive Gift Packaging",
      ],
    },
  },

  // Heritage Section
  heritage: {
    heading: "Our Story",
    accent: "Founded by Mangalasamy P in 2022",
    subheading: "Sri Amman Bakery · Serving sweetness since 2022",
    sealText: "SRI AMMAN BAKERY · FOUNDED BY MANGALASAMY P IN 2022 · SERVING SWEETNESS SINCE 2022 · ",
    storySummary:
      "Sri Amman Bakery was founded by Mangalasamy P in 2022 with a passion for traditional sweets and bakery favourites. We bring together familiar flavours and the joy of sharing something sweet with family and friends. From classic Laddu and Mysore Pak to Jalebi, Badam Burfi, Boost Burfi, Horlicks Burfi, and Badusha, our website celebrates the sweets that make every occasion special. Serving sweetness since 2022.",
    chapters: [
      {
        title: "Our Story",
        accent: "founded by Mangalasamy P in 2022.",
        body: "Sri Amman Bakery was founded by Mangalasamy P in 2022 with a passion for traditional sweets and bakery favourites. We bring together familiar flavours and the joy of sharing something sweet with family and friends.",
        start: 0.3,
      },
      {
        title: "Seven Heritage Sweets,",
        accent: "celebrating special occasions.",
        body: "From classic Laddu and Mysore Pak to Jalebi, Badam Burfi, Boost Burfi, Horlicks Burfi, and Badusha, our website celebrates the sweets that make every occasion special.",
        start: 0.5,
      },
      {
        title: "Serving sweetness",
        accent: "since 2022.",
        body: "Handcrafted with 100% pure homemade ghee and baked fresh daily with care. Sri Amman Bakery brings together familiar flavours and the joy of sharing something sweet with family and friends.",
        start: 0.72,
      },
    ],
  },

  // Estate alias pointing to heritage
  estate: {
    heading: "Our Story",
    accent: "Founded by Mangalasamy P in 2022",
    subheading: "Sri Amman Bakery · Serving sweetness since 2022",
    sealText: "SRI AMMAN BAKERY · FOUNDED BY MANGALASAMY P IN 2022 · SERVING SWEETNESS SINCE 2022 · ",
    storySummary:
      "Sri Amman Bakery was founded by Mangalasamy P in 2022 with a passion for traditional sweets and bakery favourites. We bring together familiar flavours and the joy of sharing something sweet with family and friends. From classic Laddu and Mysore Pak to Jalebi, Badam Burfi, Boost Burfi, Horlicks Burfi, and Badusha, our website celebrates the sweets that make every occasion special. Serving sweetness since 2022.",
    chapters: [
      {
        title: "Our Story",
        accent: "founded by Mangalasamy P in 2022.",
        body: "Sri Amman Bakery was founded by Mangalasamy P in 2022 with a passion for traditional sweets and bakery favourites. We bring together familiar flavours and the joy of sharing something sweet with family and friends.",
        start: 0.3,
      },
      {
        title: "Seven Heritage Sweets,",
        accent: "celebrating special occasions.",
        body: "From classic Laddu and Mysore Pak to Jalebi, Badam Burfi, Boost Burfi, Horlicks Burfi, and Badusha, our website celebrates the sweets that make every occasion special.",
        start: 0.5,
      },
      {
        title: "Serving sweetness",
        accent: "since 2022.",
        body: "Handcrafted with 100% pure homemade ghee and baked fresh daily with care. Sri Amman Bakery brings together familiar flavours and the joy of sharing something sweet with family and friends.",
        start: 0.72,
      },
    ],
  },

  // Footer Content
  footer: {
    description:
      "Handcrafted with 100% pure homemade ghee and baked fresh daily with care. Serving sweetness since 2022 with authentic traditional sweets and bakery favorites.",
    copyright: `© ${new Date().getFullYear()} Sri Amman Bakery. All rights reserved.`,
    phone: "9626758666",
    phoneDisplay: "+91 96267 58666",
    instagram: "https://www.instagram.com/sriamman_bakery/",
    whatsappChannel: "https://whatsapp.com/channel/0029Vb97jtVBadmd0d98OQ0u",
  },
};
