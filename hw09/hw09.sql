CREATE TABLE parents AS
  SELECT "abraham" AS parent, "barack" AS child UNION
  SELECT "abraham"          , "clinton"         UNION
  SELECT "delano"           , "herbert"         UNION
  SELECT "fillmore"         , "abraham"         UNION
  SELECT "fillmore"         , "delano"          UNION
  SELECT "fillmore"         , "grover"          UNION
  SELECT "eisenhower"       , "fillmore";

CREATE TABLE dogs AS
  SELECT "abraham" AS name, "long" AS fur, 26 AS height UNION
  SELECT "barack"         , "short"      , 52           UNION
  SELECT "clinton"        , "long"       , 47           UNION
  SELECT "delano"         , "long"       , 46           UNION
  SELECT "eisenhower"     , "short"      , 35           UNION
  SELECT "fillmore"       , "curly"      , 32           UNION
  SELECT "grover"         , "short"      , 28           UNION
  SELECT "herbert"        , "curly"      , 31;

CREATE TABLE sizes AS
  SELECT "toy" AS size, 24 AS min, 28 AS max UNION
  SELECT "mini"       , 28       , 35        UNION
  SELECT "medium"     , 35       , 45        UNION
  SELECT "standard"   , 45       , 60;


-- The size of each dog
CREATE TABLE size_of_dogs AS
  SELECT d.name, s.size
  FROM dogs d, sizes s
  WHERE d.height > s.min and d.height <= s.max
  ;


-- All dogs with parents ordered by decreasing height of their parent
CREATE TABLE by_parent_height AS
  SELECT d1.name 
  FROM dogs d1, parents p, dogs d2
  WHERE d1.name = p.child
  AND p.parent = d2.name
  ORDER BY d2.height DESC
  ;


-- Filling out this helper table is optional
CREATE TABLE siblings AS
  SELECT p1.parent, p1.child as child1, p2.child as child2, d1.height as height1, d2.height as height2, s1.size as size1, s2.size as size2
  FROM parents p1, parents p2, dogs d1, dogs d2, sizes s1, sizes s2
  WHERE p1.parent = p2.parent
  AND p1.child < p2.child 
  AND d1.name = p1.child 
  AND d2.name = p2.child
  AND d1.height > s1.min AND d1.height <= s1.max
  AND d2.height > s2.min AND d2.height <= s2.max
  AND s2.size = s1.size
  ;

-- Sentences about siblings that are the same size
CREATE TABLE sentences AS
  SELECT printf("The two siblings, %s plus %s have the same size: %s", child1, child2, size1)
  FROM siblings
  ;

