stdlibs = {
    # ========== STD IO ========== #
    "std/io": """
        // io.bcs
        // Coded by luke_
        // 11-11-2021
        //
        // part of the BeCauSe
        // standard library

        macro IO_WRITE 1 1 syscall3 end
        macro IO_READ swap 0 0 syscall3 end
        macro IO_EXIT 60 syscall1 end
        """
}
