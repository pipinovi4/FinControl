import {SVGProps} from "react";

const BurgerIcon = (props: SVGProps<SVGSVGElement>) => {
  return (
      <svg width="24" height="24" viewBox="0 0 24 24" {...props}>
          <path
              fill="none" stroke="currentColor" strokeLinecap="round"
              strokeLinejoin="round" strokeWidth="2" d="M4 12h16M4 18h16M4 6h16"
          />
      </svg>
  );
};

export default BurgerIcon;