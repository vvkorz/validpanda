class Helper:
    """
    Container for helper functions
    """

    @staticmethod
    def chunks(l, n):
        """
        Yield successive n-sized chunks from l.
        """
        for i in range(0, len(l), n):
            yield l[i:i + n]

    @staticmethod
    def find_pattern(header, pattern):
        """
        find pattern in the header and return the amount of columns. For example:

        pattern = 1,2,3

        header = 1,2,3,1,2,3,1,2,3,6,7,8,9

        return 9, because (1,2,3),(1,2,3),(1,2,3),6,7,8,9

        :param header: tuple where to look for patter
        :param pattern: actual pattern
        :return:
        """
        # idea is to loop over the header
        if len(header) < len(pattern):
            raise ValueError("Pattern length is bigger than a header length")
        else:
            # chunk the header into pattern sized parts
            chunked_header = list(Helper.chunks(header, len(pattern)))
            for indx, subheader in enumerate(chunked_header):
                if subheader != pattern:
                    indx = indx - 1
                    break
        return (indx+1) * len(pattern)
