import numpy as np

pi = np.pi

sectors = [(0.1326, 0.2097),
           (0.3584, 0.5481),
           (0.5883, 0.6721),
           (0.6897, 2.2968),
           (2.2973, 2.2977),
           (2.3006, 2.4000),
           (2.4049, 2.6835),
           (2.9457, 0.0949),
           (2.9468, 2.9944),
           (3.0931, 0.0498)]

out = [];
(start, end) = sectors.pop(0)
for s in sectors:
    if s[0] <= end:
        if s[1] > end:
            end = s[1]
    else:
        out.append((start, end))
        (start, end) = s

if end > pi:
    while out:
        s = out[0]
        if s[0] + pi <= end:
            out.pop(0)
            s_end = s[1] + pi
            if s_end > end:
                end = s_end
                break
        else:
            break

if end >= start + pi:
    out = [(0, pi)]
else:
    out.append((start, end))

print("merged sectors: ", out)