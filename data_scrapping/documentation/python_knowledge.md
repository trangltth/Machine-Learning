<!-- ########## class typing ####### -->
- all function in typing class is just for type hint. So user can set any types for parameters without concern type hint
    + eg: 
        from typing import List, Dict, Tuple, NewType

        Vector = List[float]

        def scale(scalar: float, vector: Vector) -> Vector:
            return [scalar * num for num in vector]

        # typechecks; a list of floats qualifies as a Vector.
        new_vector = scale(2.0, [1.0, -4.2, 5.4])
        print(new_vector)

        def scale2(scalar: float, vector: Vector) -> Vector:
            print(Vector)

        scale2(2.0, ['test', -4.2, 5.4])