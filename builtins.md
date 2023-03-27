# dREL builtin functions

The functions available for use in dREL methods are listed
below. Functions do not modify their arguments, or have any other
side-effects. Where an argument is of ’number’ type, both integers and
real numbers are accepted. These function and constant names are
reserved and may not be redefined within a dREL method or
dictionary. Where a value is passed to a function that lies outside
the acceptable domain for that function (for example, a negative
number is passed to the log function), the function returns
`NULL`. When a `missing` value is provided, the function returns
`missing`. No numerical precision considerations are relevant here;
those issues are resolved individually by dREL
implementations. Similarly, unless indicated below, any values in the
domain of the corresponding mathematical functions may be provided as
arguments without concern for overflow or underflow.

| Calling signature | Description |
| ----------------- | ----------- |
| Complex(number, integer) | Convert the two arguments Real, Imag into a complex number |
| Real(complex) | Return the real part of the complex argument |
| Imag(complex) | Return the imaginary part of the complex argument |
| Integer(number) | Convert the argument to an integer, rounding towards zero. An integer argument is returned unchanged |
| Float(number) | Convert the argument to a real number. A real argument is returned unchanged |
| Rem(number) | The remainder of a real number is returned. Zero is returned for an integer argument.|
| List(arg1,arg2,arg3,...) | Convert the arguments into a list [arg1,arg2,arg3,...] |
| Table(arg1,arg2,arg3,arg4,...) | Convert the arguments into a table {arg1:arg2, arg3:arg4,...}. Odd-numbered arguments must be strings.|
| Numb(string) | Convert the string into a number assuming ASCII encoding for digits. Decimal point is the period character.|
| Caseless(string) | Convert the string into a caseless string |
| Char(integer) | Interpret the integer argument as a Unicode code point and return the corresponding character.|
|Repr(integer) | Return a base 10 string representation of the argument. No equivalent for real numbers is currently defined.|
|Is\_missing(arg) | Return true if the argument has value `missing`. This is the only way to test for `missing`.|
| --- |
|**Mathematical functions** |
|Sin(number), Cos(number), Tan(number) | Sin, Cos and Tan of the argument in radians |
|Sind(number), Cosd(number), Tand(number) | Sin, Cos and Tan of the argument in degrees |
|Asin(number), Acos(number), Atan(number) | Arcsin, Arccos and Arctan of the argument as radians. The return value is in the range [-π/2, π/2] for asin and atan, and [0, π]for acos.|
|Asind(number), Acosd(number), Atand(number) | Arcsin, Arccos and Arctan of the argument as degrees. The return value is in the range [-90,90] for asin and atan, and [0,180] for acos|
|Atan2(number,number), Atan2d(number, number) | Arctan of argument1/argument2 in radians and degrees, respectively. The returned value will respect the quadrant as determined by the signs of the arguments.|
|Phase(complex) | The phase in radians of the complex argument.|
|Magn(number or complex) | The magnitude of the complex argument. Real or integer arguments are returned unchanged.|
|Exp(number) | $e^{argument}$ where argument is a real number.|
|ExpImag(number) | $e^{i\ argument}$ where $i=\sqrt{-1}$|
|Log(number) | The base-10 logarithm of the argument. The argument must be a real number greater than zero.|
|Ln(number) | The natural logarithm of the argument. The argument must be a real number greater than zero.|
|Pi, TwoPi | (constants) Values of π and 2π|
|Sqrt(number) | The positive square root of the real argument. If the argument is negative a complex number is returned.|
|Mod(integer,integer) | The modulus of argument1 to base argument2|
|Abs(number) | The absolute value of the real argument|
|Sign(number,number) | The sign of argument2 is applied to argument1|
|Minor(matrix) | Return a matrix of minor elements|
|Cofactor(matrix) | Return the cofactor elements of the matrix|
|Adjoint(matrix) | Generate the adjoint matrix|
|Inverse(matrix) | Generate the inverse matrix|
|Transpose(matrix) | Transpose the matrix|
|Eigen(matrix) | Calculate eigenvalues and eigenvectors of the 3x3 matrix argument. The return value is a 3-element list. Each element in this list is itself a list of 4 elements, where the first element is the eigenvalue and the next three the eigenvector.|
|Det(matrix) | Matrix determinant|
|Dot(arg1,arg2) | Dot product of the matrix arguments.|
|Cross(arg1,arg2) | Cross product of the matrix arguments. The binary operator “^” is also available|
|Norm(arg1) | The root mean square value of the elements in an array or vector|
| --- |
|**Structure examination and manipulation** |
|First(string or list), Last(string or list) | The first or last elements|
|Strip(string or list, integer) | Remove an element from the string or list, returning a new list. The second argument is the element position, counting from zero|
|Drop_missing(list) | Remove all `missing` elements from the list, returning a new list.|
|Len(string or list) | The length of the string or list|
|Indexof(list,element) | Return the zero-based index of element in list, or -1 if missing|
|Sort(list) | Sort the contents of the argument from smaller to larger, returning a new string or list|
|Reverse(string or list) | Reverse the contents of the argument, returning a new string or list|
|Dim(array) | Return an integer array of dimensions|
|Split(string,character) | Return an array of strings derived by splitting the supplied string at each occurrence of the character. The character is not included in the returned array. If no such character is present, the string is returned unchanged.|
