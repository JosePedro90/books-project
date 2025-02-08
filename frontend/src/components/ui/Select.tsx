import { createListCollection } from "@chakra-ui/react";
import {
  SelectContent,
  SelectItem,
  SelectLabel,
  SelectRoot,
  SelectTrigger,
  SelectValueText,
} from "@chakra-ui/react";

interface SelectProps {
  options: { label: string; value: string }[];
  placeholder?: string;
  label?: string;
  onChange: (value: string) => void;
  width?: string;
  height?: string;
  size?: "xs" | "sm" | "md" | "lg";
}

const Select: React.FC<SelectProps> = ({
  options,
  label,
  placeholder = "Select an option",
  onChange,
  width = "320px",
  size = "sm",
}) => {
  const handleSelectChange = (details: { value: string[] }) => {
    onChange(details.value[0]);
  };

  const listCollection = createListCollection({
    items: options,
  });

  return (
    <SelectRoot
      collection={listCollection}
      size={size}
      width={width}
      border={0}
      onValueChange={handleSelectChange}
    >
      {label && <SelectLabel>{label}</SelectLabel>}
      <SelectTrigger>
        <SelectValueText placeholder={placeholder} />
      </SelectTrigger>
      <SelectContent>
        {options.map((option) => (
          <SelectItem item={option} key={option.value} value={option.value}>
            {option.label}
          </SelectItem>
        ))}
      </SelectContent>
    </SelectRoot>
  );
};

export default Select;
