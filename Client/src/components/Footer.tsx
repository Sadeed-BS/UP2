import { Typography } from "@material-tailwind/react";
const currentYear = new Date().getFullYear();

export function Footer16() {
  return (
    <footer className=" bg-white">
      <div className="flex flex-col items-center">
        <Typography
          as="p"
          color="blue-gray"
          className="mt-6 !text-sm !font-normal text-gray-500"
          placeholder=""
          onResize={() => {}}
          onResizeCapture={() => {}}
          onPointerEnterCapture={() => {}}
          onPointerLeaveCapture={() => {}}
        >
          Copyright &copy; {currentYear} Material Tailwind
        </Typography>
      </div>
    </footer>
  );
}
export default Footer16;