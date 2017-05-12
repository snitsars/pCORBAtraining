using System;
using System.Threading;
using Ch.Elca.Iiop.Idl;

using omg.org.CORBA;
using Org.Uneta.Iiopnet.Examples.First.IHello_package;

namespace Org.Uneta.Iiopnet.Examples.First
{
    [SupportedInterface(typeof(IHello))]
    public class HelloImplementation : MarshalByRefObject, IHello
    {
        private AutoResetEvent mShutdownEvent = null;

        public HelloImplementation(AutoResetEvent shutdownEvent)
        {
            mShutdownEvent = shutdownEvent;
        }
        public void Shutdown()
        {
            mShutdownEvent.Set();
        }

        public override object InitializeLifetimeService()
        {
            return null;
        }

        public int AddValue(int a, int b)
        {
            return a + b;
        }

        [return: StringValue]
        [return: WideChar(true)]
        public string SayHello([StringValue][WideChar(true)] string name)
        {
            return "Hello, " + name + ". It's Bob.";
        }


        public void SayHello2([StringValue][WideChar(false)] string name, [StringValue][WideChar(false)] out string greeting)
        {
            greeting = "Hello, " + name + ". It's Bob.";
        }

        public bool Message([StringValue][WideChar(false)] ref string message)
        {
            if (message == "Hello, Bob")
            {
                message = "Hello, Andy.";
                return true;
            }
            return false;
        }

        public MyComplexNumber MulComplex(MyComplexNumber x, ref MyComplexNumber y)
        {
            MyComplexNumber result = new MyComplexNumber(x.re * y.re - x.im * y.im, x.re * y.im + x.im - y.re);
            y = result;
            return result;
        }


        public bool MulComplexAsAny(object x, object y, out object result)
        {
            MyComplexNumber _x = (MyComplexNumber)x;
            MyComplexNumber _y = (MyComplexNumber)y;

            MyComplexNumber _result = MulComplex(_x, ref _y);

            result = _result;
            return true;
        }


        public void DataTimeTransfer(ref long dataTimeValue)
        {
            DateTime dtServerTime = new DateTime(2016, 2, 8);
            DateTime dtFromClient = DateTime.FromFileTimeUtc(dataTimeValue);
            if (dtServerTime == dtFromClient)
            {
                dataTimeValue = dtServerTime.ToFileTimeUtc();
            }
            else
            {
                dataTimeValue = -1;
            }

        }

        public void ThrowExceptions(int excptionVariant)
        {
            switch (excptionVariant)
            {
                case 0:
                    {
                        throw new NO_IMPLEMENT(1, CompletionStatus.Completed_No);
                    }

                case 1:
                    {
                        throw new UserExceptionS();
                    }
                case 2:
                    {
                        UserExceptionExt userExceptionExt = new UserExceptionExt();
                        userExceptionExt.reason = "EXCEPTIONS_WORKS";
                        userExceptionExt.codeError = 254;
                        throw userExceptionExt;
                    }
                case 3:
                    {
                        throw new TRANSIENT();
                    }
                default:
                    {
                        throw new NotImplementedException();
                    }

            }
        }

        public bool CallMe(ITestCallBack callBack)
        {
            if (callBack != null)
                return 17 == callBack._call(10);
            else
                return false;
        }

        public int[] Reverse(int[] seq)
        {
            Array.Reverse(seq);
            return seq;
        }

        public double[] AddVectors(double[] x, double[] y)
        {
            if (x.Length != y.Length)
                throw new omg.org.CORBA.BAD_PARAM();

            double[] result = new double[x.Length];
            for (int i = 0; i < x.Length; ++i)
                result[i] = x[i] + y[i];

            return result;
        }

        public double[,] AddMatrixes(double[,] x, double[,] y)
        {
            int length = x.GetLength(0);
            int height = x.GetLength(1);

            if (length != y.GetLength(0) || height != y.GetLength(1) || x.Rank != 2 || y.Rank != 2)
            {
                throw new omg.org.CORBA.BAD_PARAM();
            }

            double[,] result = new double[length, height];
            for(int i=0; i< length; ++i)
            {
                for (int j = 0; j < height; ++j)
                {
                    result[i, j] = x[i, j] + y[i, j];
                }
            }

            return result;
        }
    }
}
