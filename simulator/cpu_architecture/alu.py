class ALU:
    @staticmethod
    def _sign(x: int) -> int:
        return (x >> 15) & 1

    @staticmethod
    def _negate(x: int) -> int:
        return ((~x) + 1) & 0xFFFF

    @staticmethod
    def _add_raw(a: int, b: int) -> int:
        return (a + b) & 0xFFFF

    @staticmethod
    def _divmod_signed(a: int, b: int):
        neg_a, neg_b = bool(ALU._sign(a)), bool(ALU._sign(b))
        mag_a = ALU._negate(a) if neg_a else a
        mag_b = ALU._negate(b) if neg_b else b
        q, r = divmod(mag_a, mag_b)        
        if neg_a != neg_b:
            q = ALU._negate(q)
        if neg_a:
            r = ALU._negate(r)              
        return q & 0xFFFF, r & 0xFFFF

    @staticmethod
    def add(a: int, b: int):
        return ALU._add_raw(a, b)

    @staticmethod
    def sub(a: int, b: int):
        return ALU._add_raw(a, ALU._negate(b))

    @staticmethod
    def cmp_flags(a: int, b: int):
        result = ALU.sub(a, b)
        sa, sb, sr = ALU._sign(a), ALU._sign(b), ALU._sign(result)
        z = result == 0
        c = a >= b                          
        n = bool(sr)
        v = (sa != sb) and (sr != sa)       
        return z, c, n, v

    @staticmethod
    def shl(a: int, shamt: int) -> int:
        return (a << shamt) & 0xFFFF

    @staticmethod
    def shru(a: int, shamt: int) -> int:
        return a >> shamt

    @staticmethod
    def shr(a: int, shamt: int) -> int:
        if shamt == 0:
            return a
        shifted = a >> shamt
        if ALU._sign(a):
            shifted |= (0xFFFF << (16 - shamt)) & 0xFFFF
        return shifted

    @staticmethod
    def mul(a: int, b: int) -> int:
        return (a * b) & 0xFFFF

    @staticmethod
    def div(a: int, b: int) -> int:
        return ALU._divmod_signed(a, b)[0]

    @staticmethod
    def rem(a: int, b: int) -> int:
        return ALU._divmod_signed(a, b)[1]

    @staticmethod
    def divu(a: int, b: int) -> int:
        return a // b

    @staticmethod
    def remu(a: int, b: int) -> int:
        return a % b
