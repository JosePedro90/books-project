import { Box } from "@chakra-ui/react";
import { BsStar, BsStarFill, BsStarHalf } from "react-icons/bs";

const Rating: React.FC<{ rating?: number; numReviews?: number }> = ({
  rating = 0,
  numReviews = 0,
}) => {
  const roundedRating = Math.round(rating * 2) / 2;
  const stars = Array(5)
    .fill("")
    .map((_, i) => {
      if (roundedRating - i >= 1) {
        return (
          <BsStarFill key={i} style={{ marginLeft: "1" }} color="teal.500" />
        );
      }
      if (roundedRating - i === 0.5) {
        return <BsStarHalf key={i} style={{ marginLeft: "1" }} />;
      }
      return <BsStar key={i} style={{ marginLeft: "1" }} />;
    });

  return (
    <Box display="flex" alignItems="center">
      {stars}
      <Box as="span" ml="2" color="gray.600" fontSize="sm">
        {rating.toFixed(1)} ({numReviews} review{numReviews > 1 ? "s" : ""})
      </Box>
    </Box>
  );
};

export default Rating;
