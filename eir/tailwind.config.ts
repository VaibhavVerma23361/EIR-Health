import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
      animation: {
        blob: "blob 4s infinite",
        fadeIn: "fadeIn 1s ease-in",
        expand: "expand 0.8s ease-in-out forwards",
        breathe: "breathe 3s ease-in-out infinite",
        "pulse-strong": "pulseStrong 1.5s ease-in-out infinite",
        blobToAvatar: "blobToAvatar 0.7s ease-out forwards",
        "slide-in-left": "slideInLeft 0.4s ease-out",
        "slide-in-right": "slideInRight 0.4s ease-out",
        "float-slow": "floatSlow 20s ease-in-out infinite",
        "float-slower": "floatSlower 25s ease-in-out infinite",
        "float-slowest": "floatSlowest 30s ease-in-out infinite",
        "float-fast": "floatSlow 8s ease-in-out infinite",
        "float-faster": "floatSlower 10s ease-in-out infinite",
        "float-medium": "floatSlowest 12s ease-in-out infinite",
      },
      transitionDelay: {
        '500': '500ms',
        '600': '600ms',
        '800': '800ms',
        '1000': '1000ms',
      },
      scale: {
        '108': '1.08',
      },
      keyframes: {
        blob: {
          "0%, 100%": {
            transform: "translate(0, 0) scale(1)",
          },
          "25%": {
            transform: "translate(300px, -200px) scale(1.15)",
          },
          "50%": {
            transform: "translate(-300px, 300px) scale(0.85)",
          },
          "75%": {
            transform: "translate(250px, 250px) scale(1.1)",
          },
        },
        expand: {
          "0%": {
            transform: "scale(0)",
            opacity: "0",
          },
          "100%": {
            transform: "scale(1)",
            opacity: "1",
          },
        },
        breathe: {
          "0%, 100%": {
            transform: "scale(1)",
            opacity: "1",
          },
          "50%": {
            transform: "scale(1.05)",
            opacity: "0.9",
          },
        },
        pulseStrong: {
          "0%, 100%": {
            transform: "scale(1)",
            opacity: "1",
          },
          "50%": {
            transform: "scale(1.15)",
            opacity: "0.8",
          },
        },
        blobToAvatar: {
          "0%": {
            transform: "scale(0.5)",
            opacity: "0",
            filter: "blur(20px)",
          },
          "100%": {
            transform: "scale(1)",
            opacity: "1",
            filter: "blur(0px)",
          },
        },
        slideInLeft: {
          "0%": {
            transform: "translateX(-50px)",
            opacity: "0",
          },
          "100%": {
            transform: "translateX(0)",
            opacity: "1",
          },
        },
        slideInRight: {
          "0%": {
            transform: "translateX(50px)",
            opacity: "0",
          },
          "100%": {
            transform: "translateX(0)",
            opacity: "1",
          },
        },
        floatSlow: {
          "0%, 100%": {
            transform: "translate(0, 0) scale(1)",
          },
          "33%": {
            transform: "translate(50px, -50px) scale(1.1)",
          },
          "66%": {
            transform: "translate(-50px, 50px) scale(0.9)",
          },
        },
        floatSlower: {
          "0%, 100%": {
            transform: "translate(0, 0) scale(1)",
          },
          "33%": {
            transform: "translate(-60px, 60px) scale(1.05)",
          },
          "66%": {
            transform: "translate(60px, -40px) scale(0.95)",
          },
        },
        floatSlowest: {
          "0%, 100%": {
            transform: "translate(0, 0) scale(1)",
          },
          "50%": {
            transform: "translate(30px, 30px) scale(1.08)",
          },
        },
      },
    },
  },
  plugins: [],
};
export default config;
