import React from "react";
import { cn } from "../../utils/cn";

// GlowingEffect component (copy your effect code here)
const GlowingEffect = React.memo(({ className = "", ...props }) => {
  // ...your glowing effect code...
  return (
    <div className={cn("absolute inset-0 pointer-events-none", className)} />
  );
});

GlowingEffect.displayName = "GlowingEffect";

// Button component
const Button = ({ children, className = "", glow = false, ...props }) => (
  <button
    className={cn(
      "relative px-6 py-2 rounded-lg bg-gradient-to-tr from-cyan-400 to-blue-600 text-white shadow-lg hover:scale-105 transition-transform font-semibold overflow-hidden",
      className
    )}
    {...props}
  >
    {glow && <GlowingEffect />}
    <span className="relative z-10">{children}</span>
  </button>
);

export { GlowingEffect };
export default Button;
