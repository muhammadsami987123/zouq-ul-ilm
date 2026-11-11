"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import {
  FaHome,
  FaFileAlt,
  FaFileWord,
  FaFilePowerpoint,
  FaEdit,
  FaGem,
} from "react-icons/fa";

const navLinks = [
  { href: "/", label: "Home", icon: <FaHome /> },
  { href: "/notes", label: "Notes", icon: <FaFileAlt /> },
  { href: "/summary", label: "Summary", icon: <FaFileWord /> },
  { href: "/slides", label: "Slides", icon: <FaFilePowerpoint /> },
  { href: "/rewrite", label: "Rewrite", icon: <FaEdit /> },
];

export default function Navigation() {
  const pathname = usePathname();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20); // shrink after 20px scroll
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <>
      <nav
        className={`fixed top-4 left-1/2 -translate-x-1/2 z-50 
        transition-all duration-500 ease-in-out
        ${scrolled ? "w-[90%] max-w-5xl py-3" : "w-[100%] max-w-6xl py-4"}
        rounded-2xl 
        bg-gradient-to-r from-black via-blue-900/80 to-gray-900/80 
        backdrop-blur-xl border border-blue-500/30 shadow-2xl`}
      >
        <div className="flex items-center justify-between px-6">
          {/* Logo */}
          <Link
            href="/"
            className="flex items-center gap-2 cursor-pointer select-none"
          >
            <FaGem
              className={`transition-all duration-500 ${
                scrolled
                  ? "text-blue-400 text-2xl"
                  : "text-blue-400 text-3xl drop-shadow-[0_0_10px_rgba(0,0,255,0.7)]"
              }`}
            />
            <span
              className={`font-bold transition-all duration-500 ${
                scrolled ? "text-2xl text-blue-400" : "text-3xl text-blue-400"
              }`}
            >
              Gem<span className="text-slate-200">Notes</span>
            </span>
          </Link>

          {/* Nav Links */}
          <div className="flex gap-1 sm:gap-2">
            {navLinks.map(({ href, label, icon }) => (
              <Link
                key={href}
                href={href}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium 
                  transition-all duration-300 
                  text-slate-300 hover:text-blue-300 hover:bg-blue-500/10 
                  ${
                    pathname === href
                      ? "bg-blue-500/20 text-blue-300 font-bold shadow-lg"
                      : ""
                  }`}
              >
                <span className="text-lg">{icon}</span>
                <span className="hidden sm:inline">{label}</span>
              </Link>
            ))}
          </div>
        </div>
      </nav>

      {/* Spacer so content doesn't overlap */}
      <div className="h-28" />
    </>
  );
}
