#include <iostream>


class List_item
{
    public:
        List_item(int val, List_item *next): val(val), next(next) {}

        List_item *set_next(List_item *iNext) {next = iNext; return this;}

        List_item *get_next() {return next;}

        int get_val() {return val;}

    private:
        int val;
        List_item *next;
};


class Spinlock
{
    public:
        Spinlock(size_t stride):
            stride(stride)
        {
            pos = new List_item(0, NULL);
            pos->set_next(pos);
        }

        void insert(int val)
        {
            auto parent = next_pos();
            auto successor = parent->get_next();
            parent->set_next(new List_item(val, successor));
            pos = parent->get_next();
        }

        int get_after_val(int val) const
        {
            auto tmp_pos = pos;
            while (true)
            {
                if (tmp_pos->get_val() == val)
                {
                    return tmp_pos->get_next()->get_val();
                }
                else
                {
                    tmp_pos = tmp_pos->get_next();
                }
            }
        }

    private:
        List_item *next_pos()
        {
            for (size_t i=0; i<stride; i++)
            {
                pos = pos->get_next();
            }

            return pos;
        }


        List_item *pos;
        size_t stride;
};


int main(void)
{
    size_t stride = 348;
    size_t max_v = 50000000;
    Spinlock spinlock(stride);

    for (size_t i=1; i<=max_v; i++)
    {
        spinlock.insert(i);

        if (i%100000 == 0)
        {
            std::cout << i/1000 << '\n';
        }
    }

    std::cout << "Answer to part 2 is: " << spinlock.get_after_val(0) << '\n';

    return 0;
}

