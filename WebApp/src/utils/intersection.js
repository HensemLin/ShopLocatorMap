import * as turf from "@turf/turf";

function intersection(circles, options) {
  const indices = new Set();
  for (let i = 0; i < circles.length - 1; i++) {
    if (indices.has(i)) continue;

    const circle1 = circles[i];
    const circle1Center = circle1.center;
    const circle1Radius = circle1.radius;

    for (let j = i + 1; j < circles.length; j++) {
      const circle2 = circles[j];
      const circle2Center = circle2.center;
      const circle2Radius = circle2.radius;

      const isIntersect = turf.booleanOverlap(
        turf.circle(circle1Center, circle1Radius, options),
        turf.circle(circle2Center, circle2Radius, options)
      );

      if (isIntersect) {
        indices.add(i);
        indices.add(j);
        break;
      }
    }
  }
  return [...indices];
}

export default intersection;
