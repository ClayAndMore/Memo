容器云安全公司 t：https://www.aporeto.com/

文档： https://docs.aporeto.com/

api: https://github.com/aporeto-inc/gaia/blob/master/doc/documentation.md



Go library implementing the Regolithe specifications as Elemental model：

Bahamut, http server 和 eleamtail， manipulate 交互 

elemental: 数据结构， 形成 model 对象， 根据 spec 文件（里面定义一些数据结构）

v 存储 后端库 和 elemental 交互， 一切写程序的都和它作用。



Gaia ,  封装了 数据库操作 和 前端的一些 数据合法性检查

Client 端：  trieme , 拉取所有策略， 



spec 文件 ：

Stored: true, 是否存入数据库， 原理是 bson 序列化是否翻译， 

Expend



源到目的， subject - object,  

但是 Trireme 策略： src - dest, 出入栈， 策略翻译



定义外网对象，  

aporeto 策略， 



Gitnode



数据包 - 五元组 - 匹配PUContext - 策略 





### maniputator_test

``` go

func TestHTTP_RetrieveMany(t *testing.T) {

	Convey("Given I have a manipulator and a working server", t, func() {

		ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			w.Header().Set("Content-Type", "application/json")
		}))
		defer ts.Close()

		mm, _ := maniphttp.New(context.Background(), "http://127.0.0.1:12345")
		//mmm := mm.(*(maniphttp.httpManipulator))

		Convey("When I retrieve the objects", func() {

			nslist := gaia.NamespacesList{}

			mctx := manipulate.NewContext(
				context.Background(),
			)

			err := mm.RetrieveMany(mctx, &nslist)

			Convey("Then err should not be nil", func() {
				So(err, ShouldBeNil)
			})

			for _, ns := range nslist {
				fmt.Printf("%#v\n", ns)
			}
			
		})

	})
}
```

