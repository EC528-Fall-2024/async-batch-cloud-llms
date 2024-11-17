class CountData:
    def __init__(self, total_count, batch_processor_count, reverse_batch_processor_count, rate_limiter_count):
        self.total_count = total_count
        self.batch_processor_count = batch_processor_count
        self.reverse_batch_processor_count = reverse_batch_processor_count
        self.rate_limiter_count = rate_limiter_count

    @staticmethod
    def from_dict(source):
        """Creates a CountData object from a dictionary."""
        return CountData(
            total_count=source.get("total_count", 0),
            batch_processor_count=source.get("batch_processor_count", 0),
            reverse_batch_processor_count=source.get("reverse_batch_processor_count", 0),
            rate_limiter_count=source.get("rate_limiter_count", 0)
        )

    def to_dict(self):
        """Converts a CountData object into a dictionary."""
        return {
            "total_count": self.total_count,
            "batch_processor_count": self.batch_processor_count,
            "reverse_batch_processor_count": self.reverse_batch_processor_count,
            "rate_limiter_count": self.rate_limiter_count
        }

    def __repr__(self):
        return f"CountData(\
                total_count={self.total_count}, \
                batch_processor_count={self.batch_processor_count}, \
                reverse_batch_processor_count={self.reverse_batch_processor_count}, \
                rate_limiter_count={self.rate_limiter_count}\
            )"
