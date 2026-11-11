export default function Footer() {
  return (
    <footer className="footer w-full py-6 bg-black/90 text-center border-t border-slate-700/30 mt-auto">
      <div className="container mx-auto">
        <p className="text-blue-500">© {new Date().getFullYear()} GemNotes</p>
        <p className="text-xs text-slate-400 opacity-80 mt-1">
          Licensed by TSInnovators
        </p>
      </div>
    </footer>
  );
}
