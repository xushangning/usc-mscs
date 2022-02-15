1. Color scheme: Due to the large number of entities in the diagram, we choose the following color scheme to better organize entities into logical groups:
    1. Blue: Academic activities
    2. Red: Room scheduling
    3. Purple: Ordering
    4. Green: Library
    5. Black: Student rating
2. Projects and classes are made a subtype of activities, which carry room scheduling information, thus utilizing features from EER. Because the drawing tool I'm using, draw.io, doesn't support EER, the relationships are represented as one-to-one relationship with explanation in labels.
3. Assumptions
    1. One group of students corresponds to exactly one project. It is impossible for multiple groups to work on the same project.
    2. A project may be supervised by more than one instructor.
    3. Attributes are added only if absolutely necessary. For example, because it is impossible to know how each room is identified, the room entity doesn't have meaningful attributes.
